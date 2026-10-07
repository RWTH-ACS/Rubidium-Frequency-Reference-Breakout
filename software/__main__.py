from nicegui import ui,app,context
import rubidium

import gpio
import index
import plots
import subprocess

app.on_startup(gpio.startup)
app.on_shutdown
ui.run(port=9000)

