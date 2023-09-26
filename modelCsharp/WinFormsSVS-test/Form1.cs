using System.Diagnostics;
using TestModel;

namespace WinFormsSVS_test
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {

            startButton.BackColor = Color.BlueViolet;
            System.Threading.Thread.Sleep(3000);
            Test.RunTests(TestConfigData.configDict);
            
        }

    }
}