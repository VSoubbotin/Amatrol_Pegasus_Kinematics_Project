#SingleInstance, Force
SendMode Input
SetTitleMatchMode, 2
SetWorkingDir, %A_ScriptDir%
StartTime := A_TickCount
Process, Exist, Dbgview.exe
While ErrorLevel == 0
{
    Process, Exist, Dbgview.exe
}
WinActivate, DebugView
PixelGetColor, log, 70, 62
if log != 0x00FF00
{
    OutputDebug, % log
    send ^g
    send {Enter}
}
; Loop
; {
    startFound = 0
    While startFound == 0
    {
        FileRead, log, debug.log
        startFound := InStr(log, ".ECMD._STARTING_PROG")
    }
    OutputDebug, "log start"
    endFound = 0
    While endFound == 0
    {
        OutputDebug, "logging"
        posData.delete(1, 6)
        Process, Exist, Robot Simulation Software 3.exe
        if ErrorLevel != 0
        {
            StatusBarGetText, output, 4, Pegasus Robot Simulation Software
            mode = "simulation"
        } else {
            Process, Exist, Controller.exe
            if ErrorLevel != 0
            {
                ControlGetText, output, 0, Pegasus Control Software
                mode = "robot"
            } else {
                mode = "inactive"
            }
        }
        if output != "Robot not homed"
        {
            if mode = "simulation"
            {
                format := SubStr(output, 28)
                posData := StrSplit(format, ",", "Robot Tip Coordinates = () inches Pitch = Roll = degrees")
                inch := InStr(format, "inches")
                metric := InStr(format, "millimeters")
                dataMode = "xyzAB"
            } else if mode = "robot" 
            {
                posMode := InStr(output, "M")
                if posMode != 0
                {
                    posData := StrSplit(output, ",")
                    i = 0
                    While i < 5
                    {
                        i += 1
                        posData[i] := SubStr(posData[i], 6)
                    }
                    dataMode = "ABCDE"
                } else 
                {
                    posData := StrSplit(output, ",", "x y z pitch roll =")
                    dataMode = "xyzAB"
                }
            }
        }
        posData.Push(A_Tickcount - StartTime)
        writeString := ""
        i = 0
        While i < 6
        {
            i += 1
            writeString .= posData[i] . " "
        }
        OutputDebug, % writeString
        
        ; FileAppend, `n, poslog.txt
        ; FileAppend, writeString, posLog.txt
        FileRead, log, debug.log
        endFound := InStr(log, ".ECMD._STOPPING_PROG")
    }
    OutputDebug, "log end"
; }
