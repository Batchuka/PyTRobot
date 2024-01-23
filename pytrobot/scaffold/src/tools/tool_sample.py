from pytrobot import Tool, BaseTool

@Tool
class SampleTool(BaseTool):
    def use(self):
        # Implementação específica da ferramenta
        print("Using sample tool.")

    # Métodos adicionais conforme necessário