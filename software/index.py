from nicegui import ui,app,context
import gpio
from rubidium import RUBI

DEFAULT_DECIMALS = 10

DISABLED = False

# Define step sizes and labels
STEPS = [
    (0.1, 'Very Coarse'),
    (1e-2, "Coarse"),
    (1e-3, "High Medium"),
    (1e-4, "Low Medium"),
    (1e-5, "Fine"),
    (6.8126e-6, "Min")
]

value = app.storage.general["fixed_value"]

rubi = RUBI("/dev/ttyUSB1") 

pps_label = []
lock_label = []
@ui.page('/')
async def main_page():
    global pps_label, lock_label


    def set_value(new_value: float) -> None:
        global value, rubi
        if not DISABLED:
            value = rubi.value_to_float(rubi.float_to_value(new_value)) #round(value + direction * step, -int(math.log10(step)))
            value_label.text = f'{value:.{DEFAULT_DECIMALS}f}Hz'
            value_label.update()
            rubi.write_value(rubi.float_to_value(value))

        else:
            ui.notify("Setring values disabled!", type="negative")

    def adjust(step: float, direction: int) -> None:
        new_value = value + direction * step
        set_value(new_value)


    def do_save() -> None:
        """Placeholder for saving logic."""
        global rubi
        if not DISABLED:
            app.storage.general["fixed_value"] = value
            rubi.write_value_to_eeprom(rubi.float_to_value(value))
        else:
            ui.notify("Serting values disabled!", type="negative")
        ui.notify(f'Saved value: {value}', type='positive')

    # Confirmation dialog for saving
    with ui.dialog() as save_dialog:
        with ui.card().classes('items-center text-center p-4 gap-3'):
            ui.label('Confirm save').classes('text-lg font-semibold')
            confirm_label = ui.label('').classes('text-gray-600')
            with ui.row().classes('justify-center gap-4 mt-2'):
                ui.button('Cancel', on_click=save_dialog.close).props('outline')
                ui.button('Confirm', on_click=lambda: (do_save(), save_dialog.close()), color='primary')

    def open_save_dialog() -> None:
        """Open the save confirmation dialog with the current value."""
        confirm_label.text = f'Do you want to save the value {value_label.text}?'
        confirm_label.update()
        save_dialog.open()


    # Top: current value (centered)
    with ui.header().classes('justify-center'):
        value_label = ui.label(f'{value:.{DEFAULT_DECIMALS}f}Hz').classes('text-4xl font-bold')
    navigation = ui.row()
    with navigation:
        ui.link('Plots', '/plots')
    # Below: cards with different step sizes and actions
    with ui.column().classes('items-center w-full gap-6 p-4'):
        ui.label('Adjust the setting with different step sizes').classes('text-lg text-gray-600')

        with ui.row().classes('justify-center w-full gap-6'):
            for step, title in STEPS:
                with ui.card().classes('w-64'):
                    # Center everything inside the card
                    with ui.column().classes('items-center text-center gap-2 w-full'):
                        ui.label(title).classes('text-base font-semibold')
                        ui.separator().classes('w-full')
                        ui.label(f'Δ = {step} Hz').classes('text-sm text-gray-500')
                        # Center the buttons
                        with ui.row().classes('justify-center w-full gap-4 mt-2'):
                            ui.button(f'-{step}', on_click=lambda s=step: adjust(s, -1)).props('outline').classes('w-28')
                            ui.button(f'+{step}', on_click=lambda s=step: adjust(s, +1)).classes('w-28')

        # Reset and Save buttons under the cards
        with ui.row().classes('justify-center w-full gap-4 mt-2'):
            ui.button('Reset', on_click=lambda: set_value(app.storage.general["fixed_value"])).props('outline')
            ui.button('Save to EEPROM', on_click=open_save_dialog, color='primary')
        with ui.row().classes('justify-center w-full gap-4 mt-2') as container:
            pps_label.append(ui.icon("radio_button_unchecked").classes('text-4xl'))
            lock_label.append(ui.icon("question_mark").classes('text-4xl'))
            gpio.lock_callback(gpio.pin.LOCK.value)