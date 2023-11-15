using TestModel;

namespace ConsoleApp1
{

    internal class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        static void Main(string[] args)
        {
            Test.RunTests(TestConfigData.configDict);
        }
    }
}