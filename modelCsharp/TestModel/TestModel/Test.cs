using System.Linq;
using System.Diagnostics;
using SVSModel.Configuration;
using SVSModel;
using System.ComponentModel;
using SVSModel.Models;
using System.Text.Json;
using Microsoft.Data.Analysis;
using System.Xml.Linq;
using System.Reflection;
using System.Data;
using System;
using static System.Net.Mime.MediaTypeNames;
using System.Text.Json.Serialization;
//using ServiceStack;
//using ServiceStack.Text;
using System.Collections.Generic;
//using Nancy.Routing.Constraints;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using Microsoft.Scripting;

namespace TestModel
{
    public class Test
    {
        private static void runPythonScript()
        {
            ////just checking
            string progToRun = @"C:\Users\1989s\source\repos\SVS\modelCsharp\TestModel\testGraph\testGraph\testGraph.py";          
            Process proc = new Process();
            proc.StartInfo.FileName = "python.exe";
            proc.StartInfo.RedirectStandardOutput = true;
            proc.StartInfo.UseShellExecute = false;  
            proc.StartInfo.Arguments =progToRun;
            proc.Start();
            StreamReader sReader = proc.StandardOutput;
            proc.WaitForExit();
            Console.ReadLine();

        }
        public static void RunTests(Dictionary<string, object> _configDict)

        {
            
            //DataFrame testConfigs = Crop.LoadCoefficients("SVSModel.Data.TestConfig.csv");

            string resourceName = "TestModel.TestConfig.csv";
            var assembly = Assembly.GetExecutingAssembly();
            Stream csv = assembly.GetManifestResourceStream(resourceName);
            DataFrame allTests = DataFrame.LoadCsv(csv);

            List<string> Tests = new List<string>();

            foreach (DataFrameRow row in allTests.Rows)
            {
                Tests.Add(row[0].ToString());
            }

            foreach (string test in Tests)
            {
                int testRow = getTestRow(test, allTests);

                SVSModel.Configuration.Config _config = SetConfigFromDataFrame(test, allTests);

                Dictionary<DateTime, double> testResults = new Dictionary<DateTime, double>();
                Dictionary<DateTime, double> nApplied = new Dictionary<DateTime, double>();

                string weatherStation = allTests["WeatherStation"][testRow].ToString();
             
                MetDataDictionaries metData = ModelInterface.BuildMetDataDictionaries(_config.Prior.EstablishDate, _config.Following.HarvestDate.AddDays(1), weatherStation);

                object[,] output = Simulation.SimulateField(metData.MeanT, metData.Rain, metData.MeanPET, testResults, nApplied, _config);

                DataFrameColumn[] columns = new DataFrameColumn[13];
                List<string> OutPutHeaders = new List<string>();
                for (int i = 0; i< output.GetLength(1); i +=1)
                {
                    OutPutHeaders.Add(output[0, i].ToString());
                    if (i == 0)
                    {
                        columns[i] = new PrimitiveDataFrameColumn<DateTime>(output[0, i].ToString());
                    }
                    else
                    {
                        columns[i] = new PrimitiveDataFrameColumn<double>(output[0, i].ToString());
                    }
                }                             
               
                var newDataframe= new DataFrame(columns);
              
                for (int r = 1; r < output.GetLength(0); r += 1)
                {
                    List<KeyValuePair<string, object>> nextRow = new List<KeyValuePair<string, object>>();
                    for (int c = 0; c < output.GetLength(1); c += 1)
                    {
                        nextRow.Add(new KeyValuePair<string, object>(OutPutHeaders[c], output[r, c]));
                    }
                    newDataframe.Append(nextRow, true);
                }               

                DataFrame.SaveCsv(newDataframe, @"C:\Users\1989s\source\repos\svs\modelCsharp\TestModel\testGraph\OutputFiles\" + test + ".csv");

            }
            runPythonScript();

        }      

        public static SVSModel.Configuration.Config SetConfigFromDataFrame(string test, DataFrame allTests)
        {
            int testRow = getTestRow(test, allTests);


            List<string> coeffs = new List<string> { "InitialN",
                                                    "SoilOrder",
                                                    "SampleDepth",
                                                    "BulkDensity",
                                                    "PMNtype",
                                                    "PMN",
                                                    "Trigger",
                                                    "Efficiency",
                                                    "Splits",
                                                    "AWC",
                                                    "PrePlantRain",
                                                    "InCropRain",
                                                    "Irrigation",
                                                    "PriorCropNameFull",
                                                    "PriorSaleableYield",
                                                    "PriorFieldLoss",
                                                    "PriorDressingLoss",
                                                    "PriorMoistureContent",
                                                    "PriorEstablishDate",
                                                    "PriorEstablishStage",
                                                    "PriorHarvestDate",
                                                    "PriorHarvestStage",
                                                    "PriorResidueRemoval",
                                                    "PriorResidueIncorporation",
                                                    "CurrentCropNameFull",
                                                    "CurrentSaleableYield",
                                                    "CurrentFieldLoss",
                                                    "CurrentDressingLoss",
                                                    "CurrentMoistureContent",
                                                    "CurrentEstablishDate",
                                                    "CurrentEstablishStage",
                                                    "CurrentHarvestDate",
                                                    "CurrentHarvestStage",
                                                    "CurrentResidueRemoval",
                                                    "CurrentResidueIncorporation",
                                                    "FollowingCropNameFull",
                                                    "FollowingSaleableYield",
                                                    "FollowingFieldLoss",
                                                    "FollowingDressingLoss",
                                                    "FollowingMoistureContent",
                                                    "FollowingEstablishDate",
                                                    "FollowingEstablishStage",
                                                    "FollowingHarvestDate",
                                                    "FollowingHarvestStage",
                                                    "FollowingResidueRemoval",
                                                    "FollowingResidueIncorporation"
            };

            Dictionary<string, object> testConfigDict = new Dictionary<string, object>();
            foreach (string c in coeffs)
            {
                testConfigDict.Add(c, allTests[c][testRow]);
            }

            List<string> datesNames = new List<string>(){ "PriorEstablishDate", "PriorHarvestDate", "CurrentEstablishDate", "CurrentHarvestDate", "FollowingEstablishDate", "FollowingHarvestDate" };

            foreach (string dN in datesNames) 
            {
                float year = (float)allTests[dN.Replace("Date", "") + "Year"][testRow];
                float month = (float)allTests[dN.Replace("Date", "") + "Month"][testRow];
                float day = (float)allTests[dN.Replace("Date", "") + "Day"][testRow];

                testConfigDict[dN] = new DateTime((int)year, (int)month, (int)day);
            }

            SVSModel.Configuration.Config ret = new SVSModel.Configuration.Config(testConfigDict);

            return ret;
        }

        private static int getTestRow(string test, DataFrame allTests)
        {
            int testRow = 0;
            bool testNotFound = true;
            while (testNotFound)
            {
                if (allTests[testRow, 0].ToString() == test)
                    testNotFound = false;
                else
                    testRow += 1;
            }
            return testRow;
        }

    }
}

