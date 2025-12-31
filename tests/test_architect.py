"""
Comprehensive tests for Architecture Advisor.
"""
import pytest
from pathlib import Path
import tempfile
from sota_agent.architect import (
    ArchitectureAdvisor,
    ComplexityLevel,
    ArchitectureRecommendation,
    DocumentParser
)


class TestArchitectureAdvisor:
    """Test ArchitectureAdvisor functionality."""
    
    @pytest.fixture
    def advisor(self):
        """Create advisor instance."""
        return ArchitectureAdvisor()
    
    def test_level_1_simple_chatbot(self, advisor):
        """Test Level 1 detection for simple chatbot."""
        briefs = [
            "Build a simple FAQ bot",
            "Create a chatbot to answer questions",
            "Simple question-answer system",
        ]
        
        for brief in briefs:
            result = advisor.analyze_brief(brief)
            assert result.level in [ComplexityLevel.SIMPLE, ComplexityLevel.CONTEXTUAL]
            assert result.confidence > 0.0
    
    def test_level_2_context_aware(self, advisor):
        """Test Level 2 detection for context-aware systems."""
        briefs = [
            "Chatbot that remembers user preferences and conversation history",
            "Assistant that maintains session context",
            "System with memory of past interactions",
        ]
        
        for brief in briefs:
            result = advisor.analyze_brief(brief)
            # Should be Level 2 or higher
            assert result.level.value >= 2
    
    def test_level_3_production_api(self, advisor):
        """Test Level 3 detection for production APIs."""
        briefs = [
            "Production-ready API with 99.9% uptime and monitoring",
            "Scalable REST API with authentication and rate limiting",
            "High-performance API with caching and load balancing",
        ]
        
        for brief in briefs:
            result = advisor.analyze_brief(brief)
            assert result.level in [ComplexityLevel.PRODUCTION, ComplexityLevel.ADVANCED, ComplexityLevel.EXPERT]
    
    def test_level_4_complex_workflow(self, advisor):
        """Test Level 4 detection for complex workflows."""
        briefs = [
            "Agent that plans tasks, executes them, and learns from mistakes",
            "System that critiques its own output and improves",
            "Self-improving agent with feedback loops",
        ]
        
        for brief in briefs:
            result = advisor.analyze_brief(brief)
            assert result.level.value >= 4
    
    def test_level_5_multi_agent(self, advisor):
        """Test Level 5 detection for multi-agent systems."""
        briefs = [
            "Multiple autonomous agents that communicate and coordinate",
            "Distributed agent system with peer-to-peer communication",
            "Agent swarm working together on complex tasks",
        ]
        
        for brief in briefs:
            result = advisor.analyze_brief(brief)
            assert result.level == ComplexityLevel.EXPERT
    
    def test_confidence_scoring(self, advisor):
        """Test confidence scores are reasonable."""
        # Very clear Level 5 brief
        result = advisor.analyze_brief(
            "Multiple autonomous agents communicate using A2A protocol "
            "and coordinate via message passing to solve distributed tasks"
        )
        assert result.confidence >= 0.8  # Should be very confident
        
        # Ambiguous brief
        result = advisor.analyze_brief("Build something")
        assert result.confidence < 0.8  # Should be less confident
    
    def test_feature_recommendations(self, advisor):
        """Test that appropriate features are recommended."""
        result = advisor.analyze_brief(
            "Multi-agent system with monitoring and memory"
        )
        
        # Should recommend relevant integrations
        assert len(result.recommended_integrations) > 0
    
    def test_empty_brief(self, advisor):
        """Test handling of empty brief."""
        result = advisor.analyze_brief("")
        assert result.level == ComplexityLevel.SIMPLE  # Default fallback
    
    def test_very_short_brief(self, advisor):
        """Test handling of very short briefs."""
        result = advisor.analyze_brief("chatbot")
        assert result.level in [ComplexityLevel.SIMPLE, ComplexityLevel.CONTEXTUAL]


class TestDocumentParser:
    """Test DocumentParser functionality."""
    
    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return DocumentParser()
    
    def test_parse_text_file(self, parser):
        """Test parsing plain text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test document.\nWith multiple lines.")
            temp_path = f.name
        
        try:
            text = parser.parse_document(temp_path)
            assert "test document" in text
            assert "multiple lines" in text
        finally:
            Path(temp_path).unlink()
    
    def test_parse_markdown_file(self, parser):
        """Test parsing markdown file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Heading\n\nThis is markdown content.")
            temp_path = f.name
        
        try:
            text = parser.parse_document(temp_path)
            assert "Heading" in text
            assert "markdown content" in text
        finally:
            Path(temp_path).unlink()
    
    def test_nonexistent_file(self, parser):
        """Test handling of non-existent file."""
        with pytest.raises(FileNotFoundError):
            parser.parse_document("/nonexistent/file.txt")
    
    def test_empty_file(self, parser):
        """Test handling of empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="empty"):
                parser.parse_document(temp_path)
        finally:
            Path(temp_path).unlink()
    
    def test_unsupported_format(self, parser):
        """Test handling of unsupported file format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
            f.write("content")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Unsupported"):
                parser.parse_document(temp_path)
        finally:
            Path(temp_path).unlink()


class TestRecommendationOutput:
    """Test recommendation output and formatting."""
    
    def test_recommendation_to_dict(self):
        """Test converting recommendation to dictionary."""
        rec = ArchitectureRecommendation(
            level=ComplexityLevel.PRODUCTION,
            level_name="Production API",
            confidence=0.95,
            input_schema="APIRequest",
            output_schema="APIResponse",
            features=["monitoring", "telemetry"],
            integrations=["databricks"],
            reasoning="Production requirements detected",
            estimated_hours="8-16",
            generation_params={}
        )
        
        # Test attributes directly (not model_dump since it's a dataclass)
        assert rec.level == ComplexityLevel.PRODUCTION
        assert rec.confidence == 0.95
        assert "monitoring" in rec.features
    
    def test_recommendation_json_serialization(self):
        """Test JSON serialization of recommendation."""
        import json
        from dataclasses import asdict
        
        rec = ArchitectureRecommendation(
            level=ComplexityLevel.SIMPLE,
            level_name="Simple Chatbot",
            confidence=0.8,
            input_schema="ChatInput",
            output_schema="ChatOutput",
            features=["core"],
            integrations=[],
            reasoning="Simple chatbot",
            estimated_hours="2-4",
            generation_params={}
        )
        
        # Convert dataclass to dict, handling Enum
        rec_dict = asdict(rec)
        rec_dict['level'] = rec.level.name  # Convert enum to string
        json_str = json.dumps(rec_dict)
        assert "SIMPLE" in json_str or "Simple" in json_str
        assert "ChatInput" in json_str


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    @pytest.fixture
    def advisor(self):
        return ArchitectureAdvisor()
    
    def test_very_long_brief(self, advisor):
        """Test with very long brief."""
        long_brief = " ".join(["word"] * 10000)
        result = advisor.analyze_brief(long_brief)
        assert result.level is not None
    
    def test_special_characters(self, advisor):
        """Test with special characters in brief."""
        brief = "Build agent with @#$% special chars & symbols!"
        result = advisor.analyze_brief(brief)
        assert result.level is not None
    
    def test_unicode_characters(self, advisor):
        """Test with unicode characters."""
        brief = "Build chatbot in 中文 with émojis 🤖"
        result = advisor.analyze_brief(brief)
        assert result.level is not None
    
    def test_mixed_level_indicators(self, advisor):
        """Test brief with indicators from multiple levels."""
        brief = """
        Simple chatbot (Level 1) with memory (Level 2),
        production API (Level 3), self-improvement (Level 4),
        and multi-agent coordination (Level 5)
        """
        result = advisor.analyze_brief(brief)
        # Should pick highest level
        assert result.level.value >= 4

