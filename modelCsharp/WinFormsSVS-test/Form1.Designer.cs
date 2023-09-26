namespace WinFormsSVS_test
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            startButton = new Button();
            lblHelloWorld = new Label();
            SuspendLayout();
            // 
            // startButton
            // 
            startButton.Font = new Font("Segoe UI", 15F, FontStyle.Regular, GraphicsUnit.Point);
            startButton.Location = new Point(157, 83);
            startButton.Name = "startButton";
            startButton.Size = new Size(318, 164);
            startButton.TabIndex = 0;
            startButton.Text = "Start Project";
            startButton.UseVisualStyleBackColor = true;
            startButton.Click += button1_Click;
            // 

            // Form1
            // 
            AutoScaleDimensions = new SizeF(10F, 25F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1156, 752);
            Controls.Add(lblHelloWorld);
            Controls.Add(startButton);
            Name = "Form1";
            Text = "Form1";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button startButton;
        private Label lblHelloWorld;
    }
}