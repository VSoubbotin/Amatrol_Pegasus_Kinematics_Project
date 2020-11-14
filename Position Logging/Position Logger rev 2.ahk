#SingleInstance, Force ; only one running
SendMode Input
SetTitleMatchMode, 2 ; partial title match mode
SetWorkingDir, %A_ScriptDir% ; files stored in same directory as script
DebugViewOutput = state.log ; debug detect file
DataOutput = posLog.txt ; output file
loop
{
    mode = "inactive"
    Process, Exist, Robot Simulation Software 3.exe ; detect if simulation or robot
    if ErrorLevel = 0 ; no simulation program
    {
        while ErrorLevel = 0
        {
            Process, Exist, Controller.exe
        }
        color = 0x878787
        while color = 0x878787
        {
            if WinActive("Pegasus Control Software")
            {
                PixelGetColor, color, 1000, 80
            }
        }
        
        mode = "robot"
    } else { ; simulation program detected
        mode = "simulation"
        Process, Exist, Dbgview.exe ; detects existing debugger
        If ErrorLevel != 0
        {
            Process, Close, Dbgview.exe ; closes existing debugger to ensure correct toggle setting
        }
        WinWaitClose, DebugViewD ; make sure file isn't deleted before debugger is closed, because it won't acutally delete and will cause false positive start detection
        FileDelete, %DebugViewOutput% ; delete old detect file
        Run, Dbgview.exe, %A_WorkingDir% ; open new debugger
        WinWait, DebugView ; wait till fully open to ensure proper input
        WinActivate, DebugView ; select debugger window
        Send ^g ; turn on log to file
        Send %A_WorkingDir%\%DebugViewOutput% ; set log file directory and name
        Send {Enter} ; enter above input
        
        log := "" ; reset read log file
        While startFound = 0 ; loop until start command found in debug log
        {
            FileRead, log, %DebugViewOutput% ; read log file
            startFound := InStr(log, ".ECMD._STARTING_PROG") ; search log file for start command
        }
    }
    startFound = 0 ; reset start detection
    endFound = 0 ; reset end detection
    FileDelete, %DataOutput% ; delete old output file if run multiple times
    rawData := [] ; clear position data
    timeStamp := [] ; clear time data
    OutputDebug, "log start"
    StartTime := A_TickCount ; program start detection time
    While endFound = 0 ; loop until end command found in debug log
    {
        OutputDebug, "logging"
        if mode = "robot"
        {
            WinActivate, Pegasus Control Software
            color = 0
            if WinActive("Pegasus Control Software")
            {
                PixelGetColor, color, 1000, 80
                if color = 0x878787
                {
                    endFound = 1
                }
            }
            ControlGetText, output, 0, Pegasus Control Software ; get position list from control software
        } else
        {
            FileRead, log, %DebugViewOutput% ; read log file
            endFound := InStr(log, ".ECMD._STOPPING_PROG") ; search log file for end command
            StatusBarGetText, output, 4, Pegasus Robot Simulation Software ; get position data from simulation software status bar
        }
        if rawData[rawData.MaxIndex()] != output ; only append if the values have changed since last loop
        {
            rawData.push(output) ; add raw read output
            timeStamp.push(A_TickCount - StartTime) ; add timestamp for reference relative to startime
            OutputDebug, % output
        }   
    }
    OutputDebug, "log end"
    OutputDebug, "Convert Data"
    i = 0
    while i < rawData.Length() ; loop for every item in data list
    {
        OutputDebug, "converting"
        i += 1
        posData.Delete(1, posData.Length()) ; clear temporary list
        if mode = "simulation"
        {
            format := SubStr(rawData[i], 28) ; remove text beginning
            posData := StrSplit(format, ",", "Robot Tip Coordinates = () inches Pitch = Roll = degrees") ; split string into array and remove irrelevant characters
            inch := InStr(format, "inches") ; detect units
            metric := InStr(format, "millimeters")
            dataMode = "xyzAB" ; data format x y z pitch roll
        } else if mode = "robot" 
        {
            posMode := InStr(rawData[i], "M") ; detect encoder data format
            OutputDebug, % posMode
            if posMode != 0
            {
                posData := StrSplit(rawData[i], ",") ; split data
                n = 0
                While n < 5
                {
                    n += 1
                    posData[n] := SubStr(posData[n], 6) ; remove irrelevant labels
                }
                dataMode = "ABCDE" ; data format encoder positions
            } else 
            {
                posData := StrSplit(output, ",", "x y z pitch roll =") ; split string into array and remove irrelevant characters
                dataMode = "xyzAB" ; data format x y z pitch roll
            }
        }
        posData.Push(timeStamp[i]) ; add time (ms) to data list
        writeString := ""
        n = 0
        While n < posData.Length()
        {
            n += 1
            writeString .= posData[n] . " " ; concatentate all of data list seperated by spaces
        }
        FileAppend, ; append dataline to output file
        (
        %writeString%

        ), %DataOutput%
    }
}
