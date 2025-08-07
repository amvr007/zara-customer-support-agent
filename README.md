Zara AI Assistant
=================

Overview
--------

Intelligent customer service agent with **dual functionality**: comprehensive support assistance and personalized product recommendations.

Core Capabilities
-----------------

###  **Customer Support Agent**

*   Product information and availability
    
*   Store policies (returns, exchanges, shipping)
    
*   Order tracking and account assistance
    
*   Size guides and fitting advice
    

### **Recommendation System**

*   Content-based product filtering using LLMs
    
*   Semantic search through product catalog
    
*   Personalized suggestions based on style preferences
    
*   Occasion and lifestyle-based recommendations
    

Architecture
------------

**Single Agent, Dual Purpose**: Seamlessly switches between support and recommendations based on user intent.

Tech Stack
----------

*   **LlamaIndex**: Vector embeddings and semantic search
    
*   **ChromaDB**: Product catalog vector storage
    
*   **OpenAI**: Text embeddings for content understanding
    
*   **Streamlit**: Customer-facing interface
    
*   **MCP Tools**: Agent-tool integration
    

Demo Scenarios
--------------

*   "What's your return policy?" → Support response
    
*   "Black dress for work meetings" → Product recommendations
    
*   "Do you have size M?" → Inventory check
    
*   "Casual weekend outfits under $50" → Filtered suggestions