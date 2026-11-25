DefinitionBlock ("", "SSDT", 2, "MECRVO", "WJ14PWR", 0x00000001)
{
    External (\_SB.BAT0, DeviceObj)
    External (\_SB.BAT0.XBTS, MethodObj)
    External (\_SB.AC0_, DeviceObj)

    Scope (\_SB.BAT0)
    {
        Method (_STA, 0, NotSerialized)
        {
            If (_OSI ("Darwin"))
            {
                Return (Zero)
            }
            Return (XBTS ())
        }
    }

    Scope (\_SB.AC0_)
    {
        Method (_STA, 0, NotSerialized)
        {
            If (_OSI ("Darwin"))
            {
                Return (Zero)
            }
            Return (0x0F)
        }
    }
}

