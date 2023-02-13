﻿using Helper;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SVSModel
{
    class SoilOrganic
    {
        /// <summary>
        /// Calculates the daily nitrogen mineralised as a result of soil organic matter decomposition
        /// </summary>
        /// <param name="simDates">series of dates over the duration of the simulation</param>
        /// <param name="meanT">A date indexed dictionary of daily mean temperatures</param>
        /// <param name="config">A specific class that holds all the simulation configuration data in the correct types for use in the model</param>
        /// <returns>Date indexed series of daily N mineralised from residues</returns>
        public static Dictionary<DateTime, double> Mineralisation(Dictionary<DateTime, double> rswc, Dictionary<DateTime, double> meanT)
        {
            DateTime[] simDates = rswc.Keys.ToArray();
            double hweon = Config.Field.HWEON;//config.Field.HWEON;
            double mrc = 0.005;

            Dictionary<DateTime, double> NSoilOM = Functions.dictMaker(simDates, new double[simDates.Length]);
            foreach (DateTime d in simDates)
            {
                double somMin = hweon * meanT[d] * rswc[d] * mrc;
                NSoilOM[d] = somMin;
            }
            return NSoilOM;
        }
    }
}