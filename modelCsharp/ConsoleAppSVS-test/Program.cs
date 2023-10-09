using TestModel;
using CommandLine;

namespace ConsoleApp1
{
    internal sealed class CommandLineOptions
    {
        [Option('b', "baseDir", Required = false, HelpText = "The path to a yaml file with the soil parameters", Default = "./")]
        public string baseDir { get; set; }

    }
    internal class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]


        protected static void RunSimulation(CommandLineOptions opts)
        {

            Console.WriteLine(opts.baseDir + "/../Config/SoilParams.yaml");

        }

        /// <summary>
        /// Handle errors with command line arguments.
        /// </summary>
        /// <param name="errs">Command line errors.</param>
        protected static void HandleParseError(IEnumerable<CommandLine.Error> errs)
        {
            Console.WriteLine("Command Line parameters provided were not valid.");
        }

        static void Main(string[] args)
        {

            Parser.Default.ParseArguments<CommandLineOptions>(args)
            .WithParsed(opts => RunSimulation(opts))
            .WithNotParsed(errs => HandleParseError(errs));

            Test.RunTests(TestConfigData.configDict);
        }
    }
}