# Terraform configuration for Databricks deployment
# Deploy SOTA Agent Framework to Databricks

terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
  }
}

provider "databricks" {
  # Configure via environment variables:
  # DATABRICKS_HOST
  # DATABRICKS_TOKEN
}

# Variables
variable "workspace_name" {
  description = "Name of the Databricks workspace"
  type        = string
  default     = "sota-agent-framework"
}

variable "catalog_name" {
  description = "Unity Catalog name"
  type        = string
  default     = "sota_agents"
}

variable "schema_name" {
  description = "Schema name in Unity Catalog"
  type        = string
  default     = "production"
}

variable "model_serving_config" {
  description = "Model serving endpoint configuration"
  type = object({
    name          = string
    model_name    = string
    model_version = string
    workload_size = string
    scale_to_zero = bool
  })
  default = {
    name          = "sota-agent-llm"
    model_name    = "gpt-4"
    model_version = "latest"
    workload_size = "Small"
    scale_to_zero = true
  }
}

# Unity Catalog - Catalog
resource "databricks_catalog" "sota_catalog" {
  name    = var.catalog_name
  comment = "SOTA Agent Framework catalog"
  properties = {
    purpose = "agent_framework"
  }
}

# Unity Catalog - Schema
resource "databricks_schema" "sota_schema" {
  catalog_name = databricks_catalog.sota_catalog.name
  name         = var.schema_name
  comment      = "Production schema for SOTA agents"
}

# Unity Catalog - Volume for prompts
resource "databricks_volume" "prompts" {
  catalog_name = databricks_catalog.sota_catalog.name
  schema_name  = databricks_schema.sota_schema.name
  name         = "prompts"
  volume_type  = "MANAGED"
  comment      = "Versioned prompts for agents"
}

# Unity Catalog - Volume for agent configs
resource "databricks_volume" "configs" {
  catalog_name = databricks_catalog.sota_catalog.name
  schema_name  = databricks_schema.sota_schema.name
  name         = "agent_configs"
  volume_type  = "MANAGED"
  comment      = "Agent configuration files"
}

# Delta table for telemetry
resource "databricks_sql_table" "telemetry" {
  catalog_name = databricks_catalog.sota_catalog.name
  schema_name  = databricks_schema.sota_schema.name
  name         = "agent_telemetry"
  table_type   = "MANAGED"
  
  column {
    name = "timestamp"
    type = "TIMESTAMP"
  }
  
  column {
    name = "agent_id"
    type = "STRING"
  }
  
  column {
    name = "trace_id"
    type = "STRING"
  }
  
  column {
    name = "span_id"
    type = "STRING"
  }
  
  column {
    name = "event_type"
    type = "STRING"
  }
  
  column {
    name = "duration_ms"
    type = "DOUBLE"
  }
  
  column {
    name = "status"
    type = "STRING"
  }
  
  column {
    name = "attributes"
    type = "MAP<STRING, STRING>"
  }
  
  comment = "Agent execution telemetry"
}

# Delta table for agent trajectories
resource "databricks_sql_table" "trajectories" {
  catalog_name = databricks_catalog.sota_catalog.name
  schema_name  = databricks_schema.sota_schema.name
  name         = "agent_trajectories"
  table_type   = "MANAGED"
  
  column {
    name = "trajectory_id"
    type = "STRING"
  }
  
  column {
    name = "agent_id"
    type = "STRING"
  }
  
  column {
    name = "timestamp"
    type = "TIMESTAMP"
  }
  
  column {
    name = "actions"
    type = "ARRAY<STRUCT<action_type:STRING,name:STRING,duration_ms:DOUBLE,cost:DOUBLE>>"
  }
  
  column {
    name = "success"
    type = "BOOLEAN"
  }
  
  column {
    name = "total_duration_ms"
    type = "DOUBLE"
  }
  
  column {
    name = "total_cost"
    type = "DOUBLE"
  }
  
  comment = "Agent execution trajectories for optimization"
}

# Model Serving Endpoint
resource "databricks_model_serving" "llm_endpoint" {
  name = var.model_serving_config.name
  
  config {
    served_models {
      model_name          = var.model_serving_config.model_name
      model_version       = var.model_serving_config.model_version
      workload_size       = var.model_serving_config.workload_size
      scale_to_zero_enabled = var.model_serving_config.scale_to_zero
    }
  }
}

# Cluster for agent execution
resource "databricks_cluster" "agent_cluster" {
  cluster_name            = "sota-agent-cluster"
  spark_version           = "13.3.x-scala2.12"
  node_type_id            = "i3.xlarge"
  autotermination_minutes = 30
  
  autoscale {
    min_workers = 1
    max_workers = 8
  }
  
  spark_conf = {
    "spark.databricks.cluster.profile" = "serverless"
    "spark.databricks.repl.allowedLanguages" = "python,sql"
  }
  
  library {
    pypi {
      package = "sota-agent-framework[all]"
    }
  }
}

# Job for batch agent processing
resource "databricks_job" "agent_batch_job" {
  name = "sota-agent-batch-processing"
  
  task {
    task_key = "process_agents"
    
    existing_cluster_id = databricks_cluster.agent_cluster.id
    
    python_wheel_task {
      package_name = "sota_agent"
      entry_point  = "run_batch"
    }
    
    library {
      pypi {
        package = "sota-agent-framework[all]"
      }
    }
  }
  
  schedule {
    quartz_cron_expression = "0 0 * * * ?" # Every hour
    timezone_id            = "UTC"
  }
}

# Outputs
output "catalog_name" {
  value = databricks_catalog.sota_catalog.name
}

output "schema_name" {
  value = databricks_schema.sota_schema.name
}

output "model_serving_endpoint" {
  value = databricks_model_serving.llm_endpoint.serving_endpoint_id
}

output "agent_cluster_id" {
  value = databricks_cluster.agent_cluster.id
}

output "telemetry_table" {
  value = "${databricks_catalog.sota_catalog.name}.${databricks_schema.sota_schema.name}.${databricks_sql_table.telemetry.name}"
}

