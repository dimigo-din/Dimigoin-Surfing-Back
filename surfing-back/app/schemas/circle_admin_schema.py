from typing import List

from pydantic import Field

from app.schemas.base_schema import BaseSchema

class NoPermissionError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class AdminSubmitResponse(BaseSchema):
    submit_id: int = Field(title="Submit ID", description="Submit ID")
    submitter_email: str = Field(title="Submitter Email", description="Submitter Email")
    question1: str = Field(title="Question 1", description="Question 1")
    question2: str = Field(title="Question 2", description="Question 2")
    question3: str = Field(title="Question 3", description="Question 3")
    question4: str = Field(title="Question 4", description="Question 4")
    status: str = Field(title="Status", description="Status")

class AdminSubmitListResponse(BaseSchema):
    submit_list: List[AdminSubmitResponse] = Field(title="Submit List", description="Submit List")

class SubmitNotFoundError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class FirstConfirmResponse(BaseSchema):
    submitter_email: str = Field(title="Submitter Email", description="Submitter Email")