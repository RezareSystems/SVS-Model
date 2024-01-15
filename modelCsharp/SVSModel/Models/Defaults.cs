using System;

namespace SVSModel.Models
{
    public class Defaults
    {
        public static readonly string PriorCropType = "Barley";
        public static readonly string PriorCropName = "Fodder";
        public static readonly string PriorVariety = "General";
        public static readonly string PriorCropNameFull = $"{PriorCropType} {PriorCropName} {PriorVariety}";

        public static readonly string CurrentCropType = "Oat";
        public static readonly string CurrentCropName = "Fodder";
        public static readonly string CurrentVariety = "General";
        public static readonly string CurrentCropNameFull = $"{CurrentCropType} {CurrentCropName} {CurrentVariety}";

        public static readonly string NextCropType = "Oat";
        public static readonly string NextCropName = "Fodder";
        public static readonly string NextVariety = "General";
        public static readonly string NextCropNameFull = $"{NextCropType} {NextCropName} {NextVariety}";

        public static readonly string EstablishStage = "Seed";
        public static readonly string HarvestStage = "EarlyReproductive";
        public static readonly double SaleableYield = 100;
        public static readonly string Units = "t/ha";

        public static readonly double FieldLoss = 0;
        public static readonly double DressingLoss = 0;
        public static readonly double MoistureContent = 9;

        public static readonly double GrowingDays = 125;
        public static readonly DateTime EstablishDate = DateTime.Today;
        public static readonly DateTime HarvestDate = DateTime.Today.AddDays(GrowingDays);

        public static readonly string ResidueRemoval = "None removed";
        public static readonly string ResidueIncorporation = "Full (Plough)";

        public static readonly string SoilOrder = "Brown";
        public static readonly string SampleDepth = "0-30cm";
        public static readonly double BulkDensity = 1.22;
        public static readonly string PMNtype = "HWEON";
        public static readonly double PMN = 60;
        public static readonly int Splits = 1;
        public static readonly string RainPrior = "Typical";
        public static readonly string RainDuring = "Typical";
        public static readonly string IrrigationApplied = "None";

        public static readonly double InitialN = 50;
        public static readonly double Trigger = 30;
        public static readonly double Efficiency = 0.8;

        public static readonly double AWC = 120;
    }
}
