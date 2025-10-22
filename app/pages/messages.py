import reflex as rx
from app.states.state import State, AuthState, MessagingState
from app.components.navbar import navbar


def message_bubble(message: dict) -> rx.Component:
    is_sender = message["sender_id"] == AuthState.user_id
    return rx.el.div(
        rx.el.div(
            rx.el.p(message["message_text"], class_name="text-sm"),
            rx.el.span(
                message["timestamp"].to_string(),
                class_name="text-xs text-gray-400 mt-1 self-end",
            ),
            class_name=rx.cond(
                is_sender,
                "bg-indigo-500 text-white p-3 rounded-lg max-w-xs flex flex-col",
                "bg-gray-200 text-gray-800 p-3 rounded-lg max-w-xs flex flex-col",
            ),
        ),
        class_name=rx.cond(
            is_sender, "flex justify-end w-full", "flex justify-start w-full"
        ),
    )


def messages_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            State.t["messages"],
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        class_name="flex items-center p-4 border-b bg-white sticky top-16 z-10",
                    ),
                    rx.el.div(
                        rx.cond(
                            MessagingState.messages.length() > 0,
                            rx.foreach(MessagingState.messages, message_bubble),
                            rx.el.div(
                                rx.el.p(
                                    State.t["no_messages_yet"],
                                    class_name="text-center text-gray-500 py-12",
                                ),
                                class_name="flex-1 flex items-center justify-center",
                            ),
                        ),
                        class_name="flex-1 p-4 space-y-4 overflow-y-auto",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.input(
                                placeholder=State.t["type_your_message"],
                                on_change=MessagingState.set_new_message_text,
                                class_name="flex-1 px-4 py-2 bg-white border border-gray-300 rounded-full focus:outline-none focus:ring-indigo-500",
                                default_value=MessagingState.new_message_text,
                            ),
                            rx.el.button(
                                rx.icon("send", class_name="h-5 w-5"),
                                on_click=MessagingState.send_message,
                                class_name="p-3 rounded-full bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50",
                                disabled=~MessagingState.new_message_text.strip().length()
                                > 0,
                            ),
                            class_name="flex items-center gap-2 p-4 border-t bg-gray-50",
                        ),
                        class_name="sticky bottom-0",
                    ),
                    class_name="flex flex-col h-[calc(100vh-64px)]",
                ),
                class_name="max-w-4xl mx-auto bg-white border-l border-r",
            ),
            on_mount=MessagingState.load_conversation,
        ),
        class_name="bg-gray-100",
    )