def laundry_symphony(buttons,presses):
    output = []
    
    counters = []
    n_settings = []
    for button in buttons:
        n_settings.append(len(button))
        counters.append(0)
    
    for press in presses:
        if isinstance(press,int):
            if press>-1: 
                if press<len(buttons):
                    button_index = press
                    output.append(buttons[button_index][counters[press]%n_settings[press]])
                    counters[press] +=1
        else:
            print("you can't press that button!")
            break
    
    return output

button_L = ['Do','Mi','So']

button_C =  ['Do','Re','Mi']

button_R =  ['Do','Re','Mi','Fa','So','La','Ti']

presses = [0,1,2,0,1,2,0,1,2,0,1,2]

song1 = laundry_symphony([button_L,button_C,button_R],presses)

print(song1)