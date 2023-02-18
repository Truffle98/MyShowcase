<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class Passwords
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()>
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()>
    Private Sub InitializeComponent()
        Me.SaveInfo = New System.Windows.Forms.Button()
        Me.InfoNameBox = New System.Windows.Forms.TextBox()
        Me.LoadUser = New System.Windows.Forms.Button()
        Me.KeyBox = New System.Windows.Forms.TextBox()
        Me.PasswordBox = New System.Windows.Forms.TextBox()
        Me.AdvancedOptionBox = New System.Windows.Forms.CheckBox()
        Me.CharacterLimit = New System.Windows.Forms.TextBox()
        Me.EnableNumbers = New System.Windows.Forms.CheckBox()
        Me.SpecialChars = New System.Windows.Forms.CheckBox()
        Me.CharLimit = New System.Windows.Forms.CheckBox()
        Me.ShowKey = New System.Windows.Forms.CheckBox()
        Me.FolderBrowserDialog1 = New System.Windows.Forms.FolderBrowserDialog()
        Me.DataList = New System.Windows.Forms.ListBox()
        Me.EnterKey = New System.Windows.Forms.Button()
        Me.UsernameBox = New System.Windows.Forms.TextBox()
        Me.LoadPassword = New System.Windows.Forms.Button()
        Me.DeleteInfo = New System.Windows.Forms.Button()
        Me.LoadBoth = New System.Windows.Forms.Button()
        Me.SuspendLayout()
        '
        'SaveInfo
        '
        Me.SaveInfo.Location = New System.Drawing.Point(40, 48)
        Me.SaveInfo.Name = "SaveInfo"
        Me.SaveInfo.Size = New System.Drawing.Size(242, 82)
        Me.SaveInfo.TabIndex = 0
        Me.SaveInfo.Text = "Save Info"
        Me.SaveInfo.UseVisualStyleBackColor = True
        '
        'InfoNameBox
        '
        Me.InfoNameBox.Location = New System.Drawing.Point(182, 156)
        Me.InfoNameBox.Name = "InfoNameBox"
        Me.InfoNameBox.Size = New System.Drawing.Size(100, 20)
        Me.InfoNameBox.TabIndex = 1
        Me.InfoNameBox.Text = "Info Name"
        '
        'LoadUser
        '
        Me.LoadUser.Location = New System.Drawing.Point(545, 48)
        Me.LoadUser.Name = "LoadUser"
        Me.LoadUser.Size = New System.Drawing.Size(99, 37)
        Me.LoadUser.TabIndex = 10
        Me.LoadUser.Text = "Load Username"
        Me.LoadUser.UseVisualStyleBackColor = True
        '
        'KeyBox
        '
        Me.KeyBox.Location = New System.Drawing.Point(544, 156)
        Me.KeyBox.Name = "KeyBox"
        Me.KeyBox.PasswordChar = Global.Microsoft.VisualBasic.ChrW(42)
        Me.KeyBox.Size = New System.Drawing.Size(100, 20)
        Me.KeyBox.TabIndex = 13
        '
        'PasswordBox
        '
        Me.PasswordBox.Location = New System.Drawing.Point(182, 205)
        Me.PasswordBox.Name = "PasswordBox"
        Me.PasswordBox.Size = New System.Drawing.Size(100, 20)
        Me.PasswordBox.TabIndex = 3
        Me.PasswordBox.Text = "Password"
        '
        'AdvancedOptionBox
        '
        Me.AdvancedOptionBox.AutoSize = True
        Me.AdvancedOptionBox.Location = New System.Drawing.Point(12, 156)
        Me.AdvancedOptionBox.Name = "AdvancedOptionBox"
        Me.AdvancedOptionBox.Size = New System.Drawing.Size(163, 17)
        Me.AdvancedOptionBox.TabIndex = 4
        Me.AdvancedOptionBox.Text = "Advanced Password Options"
        Me.AdvancedOptionBox.UseVisualStyleBackColor = True
        '
        'CharacterLimit
        '
        Me.CharacterLimit.Location = New System.Drawing.Point(40, 257)
        Me.CharacterLimit.Name = "CharacterLimit"
        Me.CharacterLimit.Size = New System.Drawing.Size(36, 20)
        Me.CharacterLimit.TabIndex = 8
        Me.CharacterLimit.Text = "20"
        Me.CharacterLimit.Visible = False
        '
        'EnableNumbers
        '
        Me.EnableNumbers.AutoSize = True
        Me.EnableNumbers.Checked = True
        Me.EnableNumbers.CheckState = System.Windows.Forms.CheckState.Checked
        Me.EnableNumbers.Location = New System.Drawing.Point(40, 185)
        Me.EnableNumbers.Name = "EnableNumbers"
        Me.EnableNumbers.Size = New System.Drawing.Size(68, 17)
        Me.EnableNumbers.TabIndex = 5
        Me.EnableNumbers.Text = "Numbers"
        Me.EnableNumbers.UseVisualStyleBackColor = True
        Me.EnableNumbers.Visible = False
        '
        'SpecialChars
        '
        Me.SpecialChars.AutoSize = True
        Me.SpecialChars.Location = New System.Drawing.Point(40, 208)
        Me.SpecialChars.Name = "SpecialChars"
        Me.SpecialChars.Size = New System.Drawing.Size(115, 17)
        Me.SpecialChars.TabIndex = 6
        Me.SpecialChars.Text = "Special Characters"
        Me.SpecialChars.UseVisualStyleBackColor = True
        Me.SpecialChars.Visible = False
        '
        'CharLimit
        '
        Me.CharLimit.AutoSize = True
        Me.CharLimit.Location = New System.Drawing.Point(40, 234)
        Me.CharLimit.Name = "CharLimit"
        Me.CharLimit.Size = New System.Drawing.Size(96, 17)
        Me.CharLimit.TabIndex = 7
        Me.CharLimit.Text = "Character Limit"
        Me.CharLimit.UseVisualStyleBackColor = True
        Me.CharLimit.Visible = False
        '
        'ShowKey
        '
        Me.ShowKey.AutoSize = True
        Me.ShowKey.Location = New System.Drawing.Point(544, 182)
        Me.ShowKey.Name = "ShowKey"
        Me.ShowKey.Size = New System.Drawing.Size(74, 17)
        Me.ShowKey.TabIndex = 14
        Me.ShowKey.Text = "Show Key"
        Me.ShowKey.UseVisualStyleBackColor = True
        '
        'DataList
        '
        Me.DataList.FormattingEnabled = True
        Me.DataList.Location = New System.Drawing.Point(402, 156)
        Me.DataList.Name = "DataList"
        Me.DataList.Size = New System.Drawing.Size(136, 95)
        Me.DataList.Sorted = True
        Me.DataList.TabIndex = 12
        '
        'EnterKey
        '
        Me.EnterKey.Location = New System.Drawing.Point(544, 208)
        Me.EnterKey.Name = "EnterKey"
        Me.EnterKey.Size = New System.Drawing.Size(100, 23)
        Me.EnterKey.TabIndex = 15
        Me.EnterKey.Text = "Enter Key"
        Me.EnterKey.UseVisualStyleBackColor = True
        '
        'UsernameBox
        '
        Me.UsernameBox.Location = New System.Drawing.Point(182, 182)
        Me.UsernameBox.Name = "UsernameBox"
        Me.UsernameBox.Size = New System.Drawing.Size(100, 20)
        Me.UsernameBox.TabIndex = 2
        Me.UsernameBox.Text = "Username"
        '
        'LoadPassword
        '
        Me.LoadPassword.Location = New System.Drawing.Point(544, 91)
        Me.LoadPassword.Name = "LoadPassword"
        Me.LoadPassword.Size = New System.Drawing.Size(100, 39)
        Me.LoadPassword.TabIndex = 11
        Me.LoadPassword.Text = "Load Password"
        Me.LoadPassword.UseVisualStyleBackColor = True
        '
        'DeleteInfo
        '
        Me.DeleteInfo.Location = New System.Drawing.Point(545, 238)
        Me.DeleteInfo.Name = "DeleteInfo"
        Me.DeleteInfo.Size = New System.Drawing.Size(99, 23)
        Me.DeleteInfo.TabIndex = 16
        Me.DeleteInfo.Text = "Delete Info"
        Me.DeleteInfo.UseVisualStyleBackColor = True
        '
        'LoadBoth
        '
        Me.LoadBoth.Location = New System.Drawing.Point(402, 48)
        Me.LoadBoth.Name = "LoadBoth"
        Me.LoadBoth.Size = New System.Drawing.Size(136, 82)
        Me.LoadBoth.TabIndex = 9
        Me.LoadBoth.Text = "Load Username and Password"
        Me.LoadBoth.UseVisualStyleBackColor = True
        '
        'Passwords
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(678, 294)
        Me.Controls.Add(Me.LoadBoth)
        Me.Controls.Add(Me.DeleteInfo)
        Me.Controls.Add(Me.LoadPassword)
        Me.Controls.Add(Me.UsernameBox)
        Me.Controls.Add(Me.EnterKey)
        Me.Controls.Add(Me.DataList)
        Me.Controls.Add(Me.ShowKey)
        Me.Controls.Add(Me.CharLimit)
        Me.Controls.Add(Me.SpecialChars)
        Me.Controls.Add(Me.EnableNumbers)
        Me.Controls.Add(Me.CharacterLimit)
        Me.Controls.Add(Me.AdvancedOptionBox)
        Me.Controls.Add(Me.PasswordBox)
        Me.Controls.Add(Me.KeyBox)
        Me.Controls.Add(Me.LoadUser)
        Me.Controls.Add(Me.InfoNameBox)
        Me.Controls.Add(Me.SaveInfo)
        Me.Name = "Passwords"
        Me.Text = "Passwords"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub

    Friend WithEvents SaveInfo As Button
    Friend WithEvents InfoNameBox As TextBox
    Friend WithEvents LoadUser As Button
    Friend WithEvents KeyBox As TextBox
    Friend WithEvents PasswordBox As TextBox
    Friend WithEvents AdvancedOptionBox As CheckBox
    Friend WithEvents CharacterLimit As TextBox
    Friend WithEvents EnableNumbers As CheckBox
    Friend WithEvents SpecialChars As CheckBox
    Friend WithEvents CharLimit As CheckBox
    Friend WithEvents ShowKey As CheckBox
    Friend WithEvents FolderBrowserDialog1 As FolderBrowserDialog
    Friend WithEvents DataList As ListBox
    Friend WithEvents EnterKey As Button
    Friend WithEvents UsernameBox As TextBox
    Friend WithEvents LoadPassword As Button
    Friend WithEvents DeleteInfo As Button
    Friend WithEvents LoadBoth As Button
End Class
