.286							   
.model TINY						   
extrn				_BootMain:near	   
.code   
org				07c00h		   ; for BootSector
main:
				jmp short start	   ; go to main
				nop
						
start:	
        cli
        mov ax,cs              
        mov ds,ax               
        mov es,ax               
        mov ss,ax                     
        mov bp,7c00h
        mov sp,7c00h           
        sti
                                
        call           _BootMain
        ret
        
        END main               
