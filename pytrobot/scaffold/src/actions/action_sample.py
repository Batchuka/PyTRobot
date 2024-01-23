from pytrobot import Action, BaseAction

@Action
class SampleAction(BaseAction):
    def perform(self):
        # Implementação específica da ação
        print("Performing sample action.")

    def on_success(self):
        # Implementação do que fazer em caso de sucesso
        print("Sample action succeeded.")

    def on_failure(self, error):
        # Implementação do que fazer em caso de falha
        print(f"Sample action failed with error: {error}")