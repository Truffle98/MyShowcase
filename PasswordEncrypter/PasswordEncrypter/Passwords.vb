Imports System.Security.Cryptography

Public Class Passwords

    Dim path As String
    Dim rand As New Random(My.Computer.Clock.TickCount)
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles SaveInfo.Click

        Dim enteredKey As String
        enteredKey = KeyBox.Text

        If enteredKey = "" Then
            MsgBox("Enter a key", 0, "Error")
            Exit Sub
        End If

        Dim infoName As String
        infoName = InfoNameBox.Text
        Dim password As String
        password = PasswordBox.Text
        Dim username As String
        username = UsernameBox.Text
        Dim wrapper As New Simple3Des(enteredKey)

        'Dim oldText As String
        'oldText = My.Computer.FileSystem.ReadAllText("D:\Games\Notes\Encrypted\Data.txt")
        'MsgBox(oldText)

        Dim fileReader As System.IO.StreamReader
        fileReader = My.Computer.FileSystem.OpenTextFileReader(path)
        Dim temp As String
        Dim compare As String

        Do
            compare = fileReader.ReadLine()
            If compare IsNot Nothing Then
                Try
                    Dim plainText As String = wrapper.DecryptData(compare)
                    If plainText = infoName Then
                        MsgBox("You already saved info under this name")
                        fileReader.Close()
                        Exit Sub
                    End If
                Catch ex As System.Security.Cryptography.CryptographicException
                    'MsgBox("The data could not be decrypted with the password.")
                End Try
            End If
            temp = fileReader.ReadLine()
            temp = fileReader.ReadLine()

        Loop Until compare Is Nothing
        fileReader.Close()

        If infoName = "Info Name" Or infoName = "" Then
            MsgBox("Enter info name", 0, "Error")
        Else
            If username = "" Or username = "Username" Then
                My.Computer.FileSystem.WriteAllText(path, wrapper.EncryptData(infoName) & vbCrLf & vbCrLf, True)
            Else
                My.Computer.FileSystem.WriteAllText(path, wrapper.EncryptData(infoName) & vbCrLf & wrapper.EncryptData(username) & vbCrLf, True)
            End If
            If password = "" Or password = "Password" Then
                My.Computer.FileSystem.WriteAllText(path, wrapper.EncryptData(Create_Password()) & vbCrLf, True)
            Else
                My.Computer.FileSystem.WriteAllText(path, wrapper.EncryptData(password) & vbCrLf, True)
            End If
            Update_Data()
        End If

    End Sub

    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        path = Environment.CurrentDirectory & "\SavedData.txt"
        My.Computer.FileSystem.WriteAllText(path, "", True)
    End Sub

    Function Create_Password()

        Dim i As Integer
        i = 0

        Dim newPass As String
        newPass = ""

        Dim n As Integer
        Dim upperLim As Integer
        Dim lowerLim As Integer
        Dim charCap As Integer
        Dim num As Integer
        Dim hasCap As Boolean
        Dim hasSpecial As Boolean
        Dim hasNumber As Boolean
        charCap = 20
        hasCap = False

        If EnableNumbers.Checked = True Then
            lowerLim = 0
            hasNumber = False
        Else
            lowerLim = 1
            hasNumber = True
        End If

        If SpecialChars.Checked = True Then
            upperLim = 4
            hasSpecial = False
        Else
            upperLim = 3
            hasSpecial = True
        End If

        If CharLimit.Checked = True Then
            charCap = Convert.ToInt32(CharacterLimit.Text)
        End If

        While i < charCap

            n = rand.Next(lowerLim, upperLim)

            If i = charCap - 1 And hasCap = False Then
                n = 1
            End If

            If i = charCap - 2 And hasNumber = False Then
                n = 0
            End If

            If i = charCap - 3 And hasSpecial = False Then
                n = 3
            End If

            If n = 0 Then
                newPass += Chr(rand.Next(48, 58))
            ElseIf n = 1 Then
                newPass += Chr(rand.Next(65, 91))
            ElseIf n = 2 Then
                newPass += Chr(rand.Next(97, 123))
            Else
                Do
                    num = rand.Next(33, 43)
                    If Not num = 34 Or Not num = 39 Then
                        Exit Do
                    End If
                Loop
                newPass += Chr(num)
            End If

            i += 1

        End While

        Return newPass

    End Function

    Private Sub CheckBox1_CheckedChanged(sender As Object, e As EventArgs) Handles AdvancedOptionBox.CheckedChanged
        If AdvancedOptionBox.Checked Then
            EnableNumbers.Visible = True
            SpecialChars.Visible = True
            CharLimit.Visible = True
        Else
            EnableNumbers.Visible = False
            SpecialChars.Visible = False
            CharLimit.Visible = False
        End If
    End Sub

    Private Sub CharLimit_CheckedChanged(sender As Object, e As EventArgs) Handles CharLimit.CheckedChanged
        If CharLimit.Checked = True Then
            CharacterLimit.Visible = True
        Else
            CharacterLimit.Visible = False
        End If
    End Sub

    Private Sub CharacterLimit_KeyPress(sender As Object, e As KeyPressEventArgs) Handles CharacterLimit.KeyPress
        If Asc(e.KeyChar) >= 48 And Asc(e.KeyChar) <= 57 Then

        ElseIf Asc(e.KeyChar) = 8 Then

        Else
            e.Handled = True
        End If
    End Sub

    Private Sub ShowKey_CheckedChanged(sender As Object, e As EventArgs) Handles ShowKey.CheckedChanged

        If KeyBox.PasswordChar = "*" Then
            KeyBox.PasswordChar = ""
        Else
            KeyBox.PasswordChar = "*"
        End If


    End Sub

    Private Sub EnterKey_Click(sender As Object, e As EventArgs) Handles EnterKey.Click

        Update_Data()

    End Sub

    Function Give_Info(n)

        Dim fileReader As System.IO.StreamReader
        fileReader = My.Computer.FileSystem.OpenTextFileReader(path)
        Dim infoName As String
        Dim enteredKey As String
        Dim temp As String

        enteredKey = KeyBox.Text
        Dim wrapper As New Simple3Des(enteredKey)

        Do
            infoName = fileReader.ReadLine()
            If infoName IsNot Nothing Then
                Try
                    Dim plainText As String = wrapper.DecryptData(infoName)
                    If plainText = DataList.SelectedItem.ToString() Then
                        If n = 0 Then
                            temp = wrapper.DecryptData(fileReader.ReadLine())
                            fileReader.Close()
                            Return temp
                        Else
                            temp = fileReader.ReadLine()
                            temp = wrapper.DecryptData(fileReader.ReadLine())
                            fileReader.Close()
                            Return temp
                        End If

                    End If
                Catch ex As System.Security.Cryptography.CryptographicException
                    'MsgBox("The data could not be decrypted with the password.")
                End Try
            End If
            temp = fileReader.ReadLine()
            temp = fileReader.ReadLine()

        Loop Until infoName Is Nothing
        fileReader.Close()

    End Function

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles LoadUser.Click

        If DataList.SelectedItem Is Nothing Then
            MsgBox("You do not have any info selected", 0, "Error")
            Exit Sub
        End If

        Dim username As String
        username = Give_Info(0)

        If username = "" Then
            MsgBox("You did not enter a username for this info", 0, "Username")
        Else
            Dim confirm As Integer
            confirm = MsgBox("After clicking ok the program will type out the username after a few seconds", 1, "Username")

            If confirm = 2 Then
                Exit Sub
            End If

            Threading.Thread.Sleep(3000)
            My.Computer.Keyboard.SendKeys(username)
        End If

    End Sub

    Private Sub LoadPassword_Click(sender As Object, e As EventArgs) Handles LoadPassword.Click

        If DataList.SelectedItem Is Nothing Then
            MsgBox("You do not have any info selected", 0, "Error")
            Exit Sub
        End If

        Dim password As String
        password = Give_Info(1)
        Dim confirm As Integer

        confirm = MsgBox("After clicking ok the program will type out the password after a few seconds", 1, "Password")
        If confirm = 2 Then
            Exit Sub
        End If
        Threading.Thread.Sleep(3000)
        My.Computer.Keyboard.SendKeys(password)

    End Sub

    Private Sub DeleteInfo_Click(sender As Object, e As EventArgs) Handles DeleteInfo.Click

        Dim fileReader As System.IO.StreamReader
        fileReader = My.Computer.FileSystem.OpenTextFileReader(path)
        Dim infoName As String
        Dim enteredKey As String
        Dim temp As String
        Dim confirm As Integer

        If DataList.SelectedItem Is Nothing Then
            MsgBox("You do not have any info selected", 0, "Error")
            Exit Sub
        End If

        confirm = MsgBox("Are you sure you want to delete this info?", 1, "Confirmation")
        If confirm = 2 Then
            Exit Sub
        End If

        enteredKey = KeyBox.Text
        Dim wrapper As New Simple3Des(enteredKey)

        Dim i As Integer
        i = 0

        Do
            infoName = fileReader.ReadLine()
            If infoName IsNot Nothing Then
                Try
                    Dim plainText As String = wrapper.DecryptData(infoName)
                    If plainText = DataList.SelectedItem.ToString() Then
                        fileReader.Close()
                        Exit Do
                    End If
                Catch ex As System.Security.Cryptography.CryptographicException
                    'MsgBox("The data could not be decrypted with the password.")
                End Try
            End If
            temp = fileReader.ReadLine()
            temp = fileReader.ReadLine()
            i += 3
        Loop Until infoName Is Nothing
        fileReader.Close()

        Dim lines As List(Of String) = System.IO.File.ReadAllLines(path).ToList
        lines.RemoveAt(i + 2)
        lines.RemoveAt(i + 1)
        lines.RemoveAt(i + 0)
        System.IO.File.WriteAllLines(path, lines)
        Update_Data()

    End Sub

    Private Sub LoadBoth_Click(sender As Object, e As EventArgs) Handles LoadBoth.Click

        If DataList.SelectedItem Is Nothing Then
            MsgBox("You do not have any info selected", 0, "Error")
            Exit Sub
        End If

        Dim username As String
        Dim password As String
        username = Give_Info(0)
        password = Give_Info(1)
        Dim confirm As Integer

        If username = "" Then
            MsgBox("You did not enter a username for this info", 0, "Username")
            Exit Sub
        End If

        confirm = MsgBox("After clicking ok the program will type out the username and password after a few seconds", 1, "Password")
        If confirm = 2 Then
            Exit Sub
        End If

        Threading.Thread.Sleep(3000)
        My.Computer.Keyboard.SendKeys(username)
        Threading.Thread.Sleep(3000)
        My.Computer.Keyboard.SendKeys(password)

    End Sub

    Sub Update_Data()

        Dim fileReader As System.IO.StreamReader
        fileReader = My.Computer.FileSystem.OpenTextFileReader(path)
        Dim infoName As String
        Dim enteredKey As String
        Dim temp As String

        enteredKey = KeyBox.Text
        Dim wrapper As New Simple3Des(enteredKey)

        DataList.BeginUpdate()
        DataList.Items.Clear()

        Do
            infoName = fileReader.ReadLine()
            temp = fileReader.ReadLine()
            temp = fileReader.ReadLine()
            If infoName IsNot Nothing Then
                Try
                    Dim plainText As String = wrapper.DecryptData(infoName)
                    DataList.Items.Add(plainText)
                Catch ex As System.Security.Cryptography.CryptographicException
                    'MsgBox("The data could not be decrypted with the password.")
                End Try
            End If

        Loop Until infoName Is Nothing
        DataList.EndUpdate()
        fileReader.Close()

    End Sub

End Class



Public NotInheritable Class Simple3Des

    Private TripleDes As New TripleDESCryptoServiceProvider

    Private Function TruncateHash(
    ByVal key As String,
    ByVal length As Integer) As Byte()

        Dim sha1 As New SHA1CryptoServiceProvider

        ' Hash the key.
        Dim keyBytes() As Byte =
            System.Text.Encoding.Unicode.GetBytes(key)
        Dim hash() As Byte = sha1.ComputeHash(keyBytes)

        ' Truncate or pad the hash.
        ReDim Preserve hash(length - 1)
        Return hash
    End Function

    Sub New(ByVal key As String)
        ' Initialize the crypto provider.
        TripleDes.Key = TruncateHash(key, TripleDes.KeySize \ 8)
        TripleDes.IV = TruncateHash("", TripleDes.BlockSize \ 8)
    End Sub

    Public Function EncryptData(
    ByVal plaintext As String) As String

        ' Convert the plaintext string to a byte array.
        Dim plaintextBytes() As Byte =
            System.Text.Encoding.Unicode.GetBytes(plaintext)

        ' Create the stream.
        Dim ms As New System.IO.MemoryStream
        ' Create the encoder to write to the stream.
        Dim encStream As New CryptoStream(ms,
            TripleDes.CreateEncryptor(),
            System.Security.Cryptography.CryptoStreamMode.Write)

        ' Use the crypto stream to write the byte array to the stream.
        encStream.Write(plaintextBytes, 0, plaintextBytes.Length)
        encStream.FlushFinalBlock()

        ' Convert the encrypted stream to a printable string.
        Return Convert.ToBase64String(ms.ToArray)
    End Function

    Public Function DecryptData(
    ByVal encryptedtext As String) As String

        ' Convert the encrypted text string to a byte array.
        Dim encryptedBytes() As Byte = Convert.FromBase64String(encryptedtext)

        ' Create the stream.
        Dim ms As New System.IO.MemoryStream
        ' Create the decoder to write to the stream.
        Dim decStream As New CryptoStream(ms,
            TripleDes.CreateDecryptor(),
            System.Security.Cryptography.CryptoStreamMode.Write)

        ' Use the crypto stream to write the byte array to the stream.
        decStream.Write(encryptedBytes, 0, encryptedBytes.Length)
        decStream.FlushFinalBlock()

        ' Convert the plaintext stream to a string.
        Return System.Text.Encoding.Unicode.GetString(ms.ToArray)
    End Function

End Class
