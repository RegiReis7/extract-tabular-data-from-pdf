from pydantic import BaseModel,Field

class Invoice(BaseModel):
    """Information about the invoice data"""
    
    product_or_service_description: str = Field(..., description="The product or service description")
    
    date: str = Field(..., description="The date of the invoice")
    
    tax_base: str = Field(..., description="The tax base amount")
    
    total: str = Field(..., description="The total amount in USD")