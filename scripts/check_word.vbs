On Error Resume Next
Set wd = GetObject(, "Word.Application")
If Err.Number <> 0 Then
    WScript.Echo "Error: " & Err.Description
Else
    WScript.Echo "Connected to Word! Docs: " & wd.Documents.Count
    For i = 1 To wd.Documents.Count
        WScript.Echo "Doc " & i & ": " & wd.Documents.Item(i).FullName & " (Saved: " & wd.Documents.Item(i).Saved & ")"
    Next
End If
