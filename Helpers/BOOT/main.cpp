#include "CDisplay.h"

#define HELLO_STR               "\"Were Ready To Boot Up! Run the Boot From Utils to complete.\"10s Till Automatic Shutdown"

extern "C" void BootMain(){
    CDisplay::ClearScreen();
    CDisplay::ShowCursor(false);

    CDisplay::TextOut(HELLO_STR,0,0,BLACK,WHITE,false);

    return true;
}
