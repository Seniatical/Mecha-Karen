// CString.h 

#ifndef __CSTRING__
#define __CSTRING__

#include "Types.h"

class CString 
{
public:
    static byte Strlen(
        const char far* inStrSource 
        );
};

#endif // __CSTRING__

// CString.cpp

#include "CString.h"

byte CString::Strlen(
        const char far* inStrSource 
        )
{
        byte lenghtOfString = 0;
        
        while(*inStrSource++ != '\0')
        {
            ++lenghtOfString;
        }
        return lenghtOfString;
}
