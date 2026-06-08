"""
Mindfighter Algorithm - Auto-Generator Logic
Core intelligence engine for intelligent content generation and transformation
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime


# ============================================================================
# ENUMS & DATA STRUCTURES
# ============================================================================

class ProcessingStrategy(Enum):
    """Strategy patterns for content generation"""
    SEMANTIC = "semantic"          # Meaning-based processing
    SYNTACTIC = "syntactic"        # Structure-based processing
    HYBRID = "hybrid"              # Combined approach
    RECURSIVE = "recursive"        # Nested generation
    ITERATIVE = "iterative"        # Loop-based refinement


class ContentType(Enum):
    """Types of content that can be generated"""
    TEXT = "text"
    CODE = "code"
    MARKDOWN = "markdown"
    JSON = "json"
    HTML = "html"
    API_RESPONSE = "api_response"


@dataclass
class GenerationContext:
    """Context for generation process"""
    input_data: Any
    strategy: ProcessingStrategy
    content_type: ContentType
    depth: int = 0
    max_depth: int = 5
    metadata: Dict[str, Any] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class GenerationResult:
    """Result from generation process"""
    output: Any
    strategy_used: ProcessingStrategy
    processing_time: float
    depth_reached: int
    transformations_applied: List[str]
    confidence_score: float
    metadata: Dict[str, Any]


# ============================================================================
# MINDFIGHTER CORE ENGINE
# ============================================================================

class MindfighterEngine:
    """
    Intelligent auto-generator using multi-strategy processing
    
    The Mindfighter algorithm combines:
    - Semantic analysis (meaning extraction)
    - Syntactic transformation (structure morphing)
    - Recursive descent (hierarchical processing)
    - Iterative refinement (quality enhancement)
    """
    
    def __init__(self):
        self.transformation_history = []
        self.cache = {}
        self.strategy_metrics = {
            ProcessingStrategy.SEMANTIC: {"uses": 0, "avg_time": 0},
            ProcessingStrategy.SYNTACTIC: {"uses": 0, "avg_time": 0},
            ProcessingStrategy.HYBRID: {"uses": 0, "avg_time": 0},
            ProcessingStrategy.RECURSIVE: {"uses": 0, "avg_time": 0},
            ProcessingStrategy.ITERATIVE: {"uses": 0, "avg_time": 0},
        }
    
    def generate(self, 
                 input_data: Any, 
                 strategy: ProcessingStrategy = ProcessingStrategy.HYBRID,
                 content_type: ContentType = ContentType.TEXT,
                 max_depth: int = 5) -> GenerationResult:
        """
        Main generation function - orchestrates the Mindfighter algorithm
        
        Args:
            input_data: Source data for generation
            strategy: Processing strategy to use
            content_type: Type of content to generate
            max_depth: Maximum recursion depth
            
        Returns:
            GenerationResult with output and metadata
        """
        
        import time
        start_time = time.time()
        
        # Create generation context
        context = GenerationContext(
            input_data=input_data,
            strategy=strategy,
            content_type=content_type,
            max_depth=max_depth
        )
        
        # Execute generation pipeline
        output, transformations = self._execute_pipeline(context)
        
        processing_time = time.time() - start_time
        confidence_score = self._calculate_confidence(output, transformations)
        
        # Create result
        result = GenerationResult(
            output=output,
            strategy_used=strategy,
            processing_time=processing_time,
            depth_reached=context.depth,
            transformations_applied=transformations,
            confidence_score=confidence_score,
            metadata={
                "input_type": type(input_data).__name__,
                "output_type": content_type.value,
                "strategy": strategy.value,
                "timestamp": context.timestamp
            }
        )
        
        # Update metrics
        self._update_metrics(strategy, processing_time)
        
        return result
    
    def _execute_pipeline(self, context: GenerationContext) -> Tuple[Any, List[str]]:
        """
        Execute the multi-stage generation pipeline
        
        Pipeline stages:
        1. Input Analysis - Understanding input structure
        2. Strategy Selection - Choosing optimal approach
        3. Transformation - Applying strategy
        4. Validation - Checking output quality
        5. Refinement - Iterative improvement
        """
        
        transformations = []
        
        # Stage 1: Input Analysis
        analysis = self._analyze_input(context.input_data)
        transformations.append(f"analyzed_{analysis['type']}")
        
        # Stage 2: Strategy Execution
        if context.strategy == ProcessingStrategy.SEMANTIC:
            output = self._semantic_transform(context, analysis)
            transformations.append("semantic_transform")
            
        elif context.strategy == ProcessingStrategy.SYNTACTIC:
            output = self._syntactic_transform(context, analysis)
            transformations.append("syntactic_transform")
            
        elif context.strategy == ProcessingStrategy.HYBRID:
            semantic_output = self._semantic_transform(context, analysis)
            syntactic_output = self._syntactic_transform(context, analysis)
            output = self._merge_transformations(semantic_output, syntactic_output)
            transformations.extend(["semantic_transform", "syntactic_transform", "merged"])
            
        elif context.strategy == ProcessingStrategy.RECURSIVE:
            output = self._recursive_transform(context, analysis)
            transformations.append("recursive_transform")
            
        elif context.strategy == ProcessingStrategy.ITERATIVE:
            output = self._iterative_refine(context, analysis)
            transformations.append("iterative_refine")
        
        # Stage 3: Content Type Formatting
        output = self._format_output(output, context.content_type)
        transformations.append(f"formatted_as_{context.content_type.value}")
        
        # Stage 4: Validation & Refinement
        if not self._validate_output(output, context.content_type):
            output = self._auto_correct(output, context.content_type)
            transformations.append("auto_corrected")
        
        return output, transformations
    
    def _analyze_input(self, input_data: Any) -> Dict[str, Any]:
        """
        Analyze input structure and characteristics
        
        Returns analysis metadata about the input
        """
        analysis = {
            "type": type(input_data).__name__,
            "is_list": isinstance(input_data, list),
            "is_dict": isinstance(input_data, dict),
            "is_string": isinstance(input_data, str),
            "length": len(input_data) if hasattr(input_data, '__len__') else 0,
            "structure": self._extract_structure(input_data),
            "complexity": self._calculate_complexity(input_data)
        }
        return analysis
    
    def _semantic_transform(self, context: GenerationContext, analysis: Dict) -> Any:
        """
        Semantic transformation - meaning-based processing
        
        Extracts semantic meaning and generates contextually relevant output
        """
        input_data = context.input_data
        
        if isinstance(input_data, dict):
            # Extract semantic concepts from dictionary
            concepts = self._extract_concepts(input_data)
            output = self._synthesize_from_concepts(concepts, analysis)
            
        elif isinstance(input_data, list):
            # Process list items semantically
            output = [self._semantic_transform(
                GenerationContext(item, context.strategy, context.content_type, 
                                context.depth + 1, context.max_depth),
                self._analyze_input(item)
            )[0] for item in input_data]
            
        elif isinstance(input_data, str):
            # Semantic analysis of text
            tokens = self._tokenize_semantic(input_data)
            output = self._generate_from_tokens(tokens)
        else:
            output = input_data
        
        return output
    
    def _syntactic_transform(self, context: GenerationContext, analysis: Dict) -> Any:
        """
        Syntactic transformation - structure-based processing
        
        Reorganizes and restructures data according to syntactic rules
        """
        input_data = context.input_data
        
        # Apply structural transformations
        if isinstance(input_data, dict):
            output = self._restructure_dict(input_data, analysis)
        elif isinstance(input_data, list):
            output = self._restructure_list(input_data, analysis)
        elif isinstance(input_data, str):
            output = self._restructure_text(input_data, analysis)
        else:
            output = input_data
        
        return output
    
    def _recursive_transform(self, context: GenerationContext, analysis: Dict) -> Any:
        """
        Recursive transformation - hierarchical nested processing
        
        Processes nested structures recursively up to max_depth
        """
        if context.depth >= context.max_depth:
            return context.input_data
        
        input_data = context.input_data
        
        if isinstance(input_data, dict):
            output = {}
            for key, value in input_data.items():
                new_context = GenerationContext(
                    value, context.strategy, context.content_type,
                    context.depth + 1, context.max_depth
                )
                output[key], _ = self._execute_pipeline(new_context)
            return output
            
        elif isinstance(input_data, list):
            output = []
            for item in input_data:
                new_context = GenerationContext(
                    item, context.strategy, context.content_type,
                    context.depth + 1, context.max_depth
                )
                result, _ = self._execute_pipeline(new_context)
                output.append(result)
            return output
        else:
            return input_data
    
    def _iterative_refine(self, context: GenerationContext, analysis: Dict) -> Any:
        """
        Iterative refinement - loop-based quality enhancement
        
        Repeatedly refines output to improve quality metrics
        """
        output = context.input_data
        refinement_passes = 3
        
        for iteration in range(refinement_passes):
            quality_before = self._measure_quality(output)
            
            # Apply refinement transformations
            output = self._apply_refinement_pass(output, iteration)
            
            quality_after = self._measure_quality(output)
            
            # Stop if quality plateaus
            if abs(quality_after - quality_before) < 0.01:
                break
        
        return output
    
    def _merge_transformations(self, semantic: Any, syntactic: Any) -> Any:
        """
        Merge results from semantic and syntactic transformations
        
        Combines both approaches for hybrid strategy
        """
        if isinstance(semantic, dict) and isinstance(syntactic, dict):
            merged = {**semantic, **syntactic}
            merged["_semantic_origin"] = semantic
            merged["_syntactic_origin"] = syntactic
            return merged
        elif isinstance(semantic, str) and isinstance(syntactic, str):
            return f"{semantic}\n{syntactic}"
        else:
            return {"semantic": semantic, "syntactic": syntactic}
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _extract_concepts(self, data: Dict) -> List[str]:
        """Extract semantic concepts from data"""
        concepts = []
        if isinstance(data, dict):
            for key, value in data.items():
                concepts.append(key)
                if isinstance(value, str):
                    concepts.extend(value.split())
        return list(set(concepts))
    
    def _synthesize_from_concepts(self, concepts: List[str], analysis: Dict) -> str:
        """Synthesize output from extracted concepts"""
        return " ".join(concepts)
    
    def _tokenize_semantic(self, text: str) -> List[str]:
        """Tokenize text into semantic units"""
        return text.split()
    
    def _generate_from_tokens(self, tokens: List[str]) -> str:
        """Generate output from tokens"""
        return " ".join(tokens)
    
    def _restructure_dict(self, data: Dict, analysis: Dict) -> Dict:
        """Restructure dictionary data"""
        return {k: str(v) for k, v in data.items()}
    
    def _restructure_list(self, data: List, analysis: Dict) -> List:
        """Restructure list data"""
        return [str(item) for item in data]
    
    def _restructure_text(self, text: str, analysis: Dict) -> str:
        """Restructure text data"""
        lines = text.split('\n')
        return '\n'.join(sorted(lines))
    
    def _apply_refinement_pass(self, data: Any, iteration: int) -> Any:
        """Apply a single refinement pass"""
        if isinstance(data, str):
            return data.upper() if iteration % 2 == 0 else data
        elif isinstance(data, dict):
            return {k: self._apply_refinement_pass(v, iteration) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._apply_refinement_pass(item, iteration) for item in data]
        return data
    
    def _format_output(self, output: Any, content_type: ContentType) -> Any:
        """Format output according to content type"""
        if content_type == ContentType.JSON:
            return json.dumps(output, indent=2)
        elif content_type == ContentType.MARKDOWN:
            return self._to_markdown(output)
        elif content_type == ContentType.HTML:
            return self._to_html(output)
        elif content_type == ContentType.CODE:
            return self._to_code(output)
        else:
            return str(output)
    
    def _to_markdown(self, data: Any) -> str:
        """Convert to markdown format"""
        if isinstance(data, dict):
            lines = ["## Data\n"]
            for k, v in data.items():
                lines.append(f"- **{k}**: {v}")
            return "\n".join(lines)
        return str(data)
    
    def _to_html(self, data: Any) -> str:
        """Convert to HTML format"""
        if isinstance(data, dict):
            items = "".join([f"<li><strong>{k}</strong>: {v}</li>" for k, v in data.items()])
            return f"<ul>{items}</ul>"
        return f"<p>{data}</p>"
    
    def _to_code(self, data: Any) -> str:
        """Convert to code format"""
        return f"# Generated Code\ndata = {repr(data)}"
    
    def _extract_structure(self, data: Any) -> str:
        """Extract structural pattern from data"""
        if isinstance(data, dict):
            return f"dict({len(data)} keys)"
        elif isinstance(data, list):
            return f"list({len(data)} items)"
        else:
            return type(data).__name__
    
    def _calculate_complexity(self, data: Any, max_depth: int = 3, depth: int = 0) -> float:
        """Calculate structural complexity (0-1 scale)"""
        if depth >= max_depth:
            return 0.0
        
        if isinstance(data, dict):
            return min(0.3 * (len(data) / 10) + 
                      sum(self._calculate_complexity(v, max_depth, depth + 1) 
                          for v in data.values()) / len(data), 1.0)
        elif isinstance(data, list):
            return min(0.3 * (len(data) / 10) + 
                      sum(self._calculate_complexity(item, max_depth, depth + 1) 
                          for item in data) / len(data), 1.0)
        else:
            return 0.1
    
    def _validate_output(self, output: Any, content_type: ContentType) -> bool:
        """Validate generated output quality"""
        if content_type == ContentType.JSON:
            try:
                json.loads(output) if isinstance(output, str) else json.dumps(output)
                return True
            except:
                return False
        elif content_type == ContentType.HTML:
            return "<" in str(output) and ">" in str(output)
        else:
            return len(str(output)) > 0
    
    def _auto_correct(self, output: Any, content_type: ContentType) -> Any:
        """Auto-correct invalid output"""
        if content_type == ContentType.JSON:
            return json.dumps({"error": "invalid", "original": str(output)})
        elif content_type == ContentType.HTML:
            return f"<div>{output}</div>"
        return output
    
    def _measure_quality(self, data: Any) -> float:
        """Measure quality of generated data (0-1 scale)"""
        if isinstance(data, str):
            return len(data) / 1000.0
        elif isinstance(data, dict):
            return min(len(data) / 100.0, 1.0)
        elif isinstance(data, list):
            return min(len(data) / 100.0, 1.0)
        return 0.5
    
    def _calculate_confidence(self, output: Any, transformations: List[str]) -> float:
        """Calculate confidence score for generation (0-1 scale)"""
        base_confidence = 0.7
        transformation_bonus = min(len(transformations) * 0.05, 0.2)
        quality = self._measure_quality(output)
        
        return min(base_confidence + transformation_bonus + (quality * 0.1), 1.0)
    
    def _update_metrics(self, strategy: ProcessingStrategy, processing_time: float):
        """Update strategy performance metrics"""
        metrics = self.strategy_metrics[strategy]
        metrics["uses"] += 1
        old_avg = metrics["avg_time"]
        metrics["avg_time"] = (old_avg * (metrics["uses"] - 1) + processing_time) / metrics["uses"]


# ============================================================================
# GLOBAL ENGINE INSTANCE
# ============================================================================

mindfighter = MindfighterEngine()


def generate(input_data: Any, 
             strategy: str = "hybrid",
             content_type: str = "text",
             max_depth: int = 5) -> Dict[str, Any]:
    """
    Public API for Mindfighter generation
    
    Args:
        input_data: Data to process
        strategy: Processing strategy ("semantic", "syntactic", "hybrid", "recursive", "iterative")
        content_type: Output type ("text", "json", "markdown", "html", "code")
        max_depth: Maximum recursion depth
        
    Returns:
        Generation result as dictionary
    """
    
    try:
        strategy_enum = ProcessingStrategy[strategy.upper()]
    except KeyError:
        strategy_enum = ProcessingStrategy.HYBRID
    
    try:
        content_type_enum = ContentType[content_type.upper()]
    except KeyError:
        content_type_enum = ContentType.TEXT
    
    result = mindfighter.generate(
        input_data=input_data,
        strategy=strategy_enum,
        content_type=content_type_enum,
        max_depth=max_depth
    )
    
    return {
        "output": result.output,
        "strategy": result.strategy_used.value,
        "processing_time": result.processing_time,
        "depth": result.depth_reached,
        "transformations": result.transformations_applied,
        "confidence": result.confidence_score,
        "metadata": result.metadata
    }
