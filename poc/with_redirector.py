# import rx
# from rx import operators as ops
# from threading import Thread
# from contextlib import contextmanager

# class EventDetectedException(Exception):
#     pass

# @contextmanager
# def event_redirector(observable):
#     def on_event(data):
#         raise EventDetectedException("Evento detectado, redirecionando o fluxo.")

#     subscription = observable.subscribe(
#         on_next=on_event,
#         on_error=lambda e: print(f"Erro: {e}"),
#     )

#     try:
#         yield
#     except EventDetectedException as e:
#         print(e)
#     finally:
#         subscription.dispose()

# # Simulação de um evento observável
# def simulate_event(observer, scheduler):
#     Thread(target=lambda: observer.on_next("Evento")).start()

# observable = rx.create(simulate_event)

# # Fluxo principal
# def main_flow():
#     print("Início do fluxo principal.")

#     with event_redirector(observable):
#         print("Executando tarefa que pode ser interrompida.")
#         # Simule a execução que aguarda um evento
#         Thread(target=lambda: rx.sleep(2)).start()

#     print("Continuação do fluxo principal após a interrupção.")

# if __name__ == "__main__":
#     main_flow()
