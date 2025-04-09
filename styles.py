class Styles:
    FONT = ('Arial', 12)
    FONT_BOLD = ('Arial', 12, 'bold')
    PADX = 10
    PADY = 5
    BG_COLOR = '#f0f0f0'
    BUTTON_COLOR = '#4A90E2'
    BUTTON_FG = 'white'

    # Estilo de botão com bordas arredondadas
    BUTTON_STYLE = {
        'font': FONT_BOLD,
        'bg': BUTTON_COLOR,
        'fg': BUTTON_FG,
        'padx': PADX,
        'pady': PADY,
        'relief': 'flat',  # Define sem borda padrão
        'bd': 0,  # Sem borda
        'highlightthickness': 0,  # Remove borda de foco
        'width': 15,
        'height': 2,
        'activebackground': BUTTON_COLOR,
        'activeforeground': 'white',
        'cursor': 'hand2'
    }   