from typing import List
from pydantic import BaseModel, Field

class Source(BaseModel):
    """Schema for a source used by agent"""
    url: str = Field(description="The url of the source")

class AgentResponse(BaseModel):
    """Schema for an agent response with anser and source"""
    answer: str = Field(description="The answer to the question")
    sources: List[Source] = Field(
        default_factory=list,
        description="List of sources used to generate the answer"
    )