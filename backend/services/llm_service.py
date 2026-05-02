import base64
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from backend.config import settings

class LLMService:
    def __init__(self):
        self.provider = settings.MODEL_PROVIDER.lower()
        self.vision_model_name = settings.VISION_MODEL
        
        if self.provider == "openai":
            self.llm = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model="gpt-4o",
                temperature=0.0
            )
            self.vision_llm = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=self.vision_model_name,
                temperature=0.0
            )
        elif self.provider == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                google_api_key=settings.GEMINI_API_KEY,
                model="gemini-1.5-pro",
                temperature=0.0
            )
            self.vision_llm = ChatGoogleGenerativeAI(
                google_api_key=settings.GEMINI_API_KEY,
                model="gemini-1.5-pro",
                temperature=0.0
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate_text(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content

    def extract_from_image(self, base64_image: str, prompt: str) -> str:
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ]
        )
        response = self.vision_llm.invoke([message])
        return response.content

llm_service = LLMService()
