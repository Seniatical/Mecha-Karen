// BootMain.cpp

#include "CDisplay.h"

#define HELLO_STR               "\"Were Ready To Boot Up! Run the Boot From Utils to complete.\", from low-level..."

extern "C" void BootMain()
{
    CDisplay::ClearScreen();
    CDisplay::ShowCursor(false);

    CDisplay::TextOut(
        HELLO_STR,
        0,
        0,
        BLACK,
        WHITE,
        false
        );

    return;
}
