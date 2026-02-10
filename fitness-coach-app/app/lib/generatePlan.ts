export function generatePlanForGoal(opts: {
  goal: string;
  weightKg: number | null;
  activity: string;
}) {
  const { goal, weightKg, activity } = opts;

  const activityBump =
    activity === "Intense" ? 200 :
    activity === "Moderate" ? 100 : 0;

  let calorieTarget = 2000 + activityBump;
  let proteinPerKgToday = 1.8;
  let todayWorkoutFocus = "Strength + Light Conditioning";
  let todayWorkoutDetails = [
    "Full Body Circuit 3 rounds:",
    "  - Squat x12",
    "  - Push-up x12",
    "  - Row x12/side",
    "Then walk 20 min easy pace",
  ];
  let todayCoachNote =
    "Stay consistent. Hit protein, move daily, sleep well. We’re aiming for long-term stability.";
  let todayMeals = [
    { label: "Breakfast", text: "Greek yogurt + granola + berries" },
    { label: "Lunch", text: "Chicken wrap with veggies and avocado" },
    { label: "Dinner", text: "Rice, veggies, lean protein" },
    { label: "Snack", text: "Protein shake or cottage cheese + fruit" },
  ];

  if (goal === "Lose Fat") {
    calorieTarget = 1800 + activityBump;
    proteinPerKgToday = 2.0;
    todayWorkoutFocus = "Full Body Strength + Walking";
    todayWorkoutDetails = [
      "Goblet Squat 3 x 12",
      "Push-ups 3 x max",
      "Row 3 x 15/side",
      "Plank 3 x 30 sec",
      "Walk 30+ min (easy pace)",
    ];
    todayCoachNote =
      "Small deficit, high protein, daily walking. We care about streaks, not perfection.";
    todayMeals = [
      { label: "Breakfast", text: "Egg whites + spinach + salsa + berries" },
      { label: "Lunch", text: "Grilled chicken salad (light dressing)" },
      { label: "Dinner", text: "Lean fish or chicken + veggies; carbs moderate" },
      { label: "Snack", text: "Greek yogurt or protein shake" },
    ];
  } else if (goal === "Build Muscle") {
    calorieTarget = 2200 + activityBump;
    proteinPerKgToday = 2.2;
    todayWorkoutFocus = "Hypertrophy Push / Pull / Legs Style Work";
    todayWorkoutDetails = [
      "Dumbbell Bench Press 4 x 8-10",
      "One-arm Row 4 x 10/side",
      "Split Squat 3 x 10/side",
      "Cable/Band Fly 3 x 12-15",
      "10-15 min easy incline walk",
    ];
    todayCoachNote =
      "Mild surplus. Lift controlled, close to failure, sleep enough. Protein across the day.";
    todayMeals = [
      { label: "Breakfast", text: "Eggs + oats + peanut butter + banana" },
      { label: "Lunch", text: "Chicken or turkey bowl with rice and veggies" },
      { label: "Dinner", text: "Salmon or beef, potatoes/rice, veggies" },
      { label: "Post-Workout", text: "Whey shake + fruit" },
    ];
  }

  const proteinTarget = weightKg ? Math.round(weightKg * proteinPerKgToday) : 140;
  const carbsTarget = 160;
  const fatTarget = 60;

  return {
    dailyTargets: { calorieTarget, proteinTarget, carbsTarget, fatTarget },
    todayMeals,
    todayWorkoutFocus,
    todayWorkoutDetails,
    todayCoachNote,

    weekMeals: [],
    weekWorkouts: [],
  };
}
