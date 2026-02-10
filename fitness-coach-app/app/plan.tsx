import { router } from "expo-router";
import React, { useEffect, useState } from "react";
import {
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

import { api } from "./lib/api";
import { getTodayActiveEnergy } from "./lib/apple/appleHealthActivityHelper";
import { requestHealthPermissions } from "./lib/apple/appleHealthPermissions";
import { getUserId } from "./lib/storage";

type MealEntry = {
  label: string;
  meal: {
    name: string;
    macros: { calories: number; protein: number; carbs: number; fat: number };
    ingredients: string[];
    instructions: string;
    tags?: string[];
  };
};

type GeneratedPlan = {
  nutritionToday: {
    calorieTarget: number;
    proteinTarget: number;
    carbsTarget: number;
    fatTarget: number;
  };
  meals: MealEntry[];
  workoutFocus: string;
  workoutDetails: string[];
  coachNote: string;
};

const trimInstruction = (txt: string) => {
  if (!txt) return "";
  if (txt.length <= 140) return txt;
  return txt.slice(0, 140).trim() + "…";
};

const weekdayKey = (["sun","mon","tue","wed","thu","fri","sat"][
  new Date().getDay()
] || "mon") as "sun"|"mon"|"tue"|"wed"|"thu"|"fri"|"sat";

const fmt = (ex: any): string => {
  const name = String(ex?.name ?? "");
  const sets = ex?.sets;
  const reps = ex?.reps;
  const time = ex?.time;

  if (!name) return "";
  if (time) return `${name} — ${time}`;
  if (sets && reps) return `${name} — ${sets} × ${reps}`;
  if (sets) return `${name} — ${sets} sets`;
  return name;
};

function mapServerToGeneratedPlan(res: any): GeneratedPlan {
  const daily = res?.daily_targets ?? {};

  const todayMeals = Array.isArray(res?.week_meals?.[weekdayKey])
    ? res.week_meals[weekdayKey]
    : [];

  const todayWorkout = res?.week_workouts?.[weekdayKey] ?? {};

  return {
    nutritionToday: {
      calorieTarget: daily.calorieTarget ?? 2000,
      proteinTarget: daily.proteinTarget ?? 120,
      carbsTarget: daily.carbsTarget ?? 160,
      fatTarget: daily.fatTarget ?? 60,
    },
    meals: todayMeals.map((m: any) => ({
      label: String(m?.label ?? "Meal"),
      meal: {
        name: m?.meal?.name ?? "",
        macros: m?.meal?.macros ?? {},
        ingredients: m?.meal?.ingredients ?? [],
        instructions: trimInstruction(m?.meal?.instructions ?? ""),
        tags: m?.meal?.tags ?? [],
      }
    })),
    workoutFocus: String(todayWorkout?.focus ?? "Rest"),
    workoutDetails: Array.isArray(todayWorkout?.details)
      ? todayWorkout.details.map(fmt).filter(Boolean)
      : [],
    coachNote: String(todayWorkout?.coachNote ?? ""),
  };
}

export default function PlanScreen() {
  const [serverPlan, setServerPlan] = useState<GeneratedPlan | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const id = await getUserId();
        if (!id) throw new Error("Missing userId");

        const res = await api.getCurrentPlan(id);
        const mapped = mapServerToGeneratedPlan(res);
        if (mounted) setServerPlan(mapped);
      } catch (e: any) {
        if (mounted) setErr(e?.message || "Unable to load plan.");
      } finally {
        if (mounted) setLoading(false);
      }
    })();

    return () => { mounted = false; };
  }, []);

  // APPLE HEALTH PERMISSION REQUEST
 
  useEffect(() => {
  requestHealthPermissions()
    .then(() => {
      return getTodayActiveEnergy();
    })
    .catch((err) => {
      console.log("HealthKit permissions denied or energy error:", err);
    });
}, []);

const plan = serverPlan;

if (!plan) {
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.headerRow}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.screenTitle}>Your Plan For Today</Text>
      </View>

      <Text style={{ color: "#94a3b8" }}>
        Waiting for server plan…
      </Text>
    </ScrollView>
  );
}

const actualTotals = plan.meals.reduce(
  (acc, m) => {
    const macros = m.meal.macros || {};
    return {
      calories: acc.calories + (macros.calories || 0),
      protein: acc.protein + (macros.protein || 0),
      carbs: acc.carbs + (macros.carbs || 0),
      fat: acc.fat + (macros.fat || 0),
    };
  },
  { calories: 0, protein: 0, carbs: 0, fat: 0 }
);

  if (!plan) {
    return (
      <ScrollView style={styles.container} contentContainerStyle={styles.content}>
        <View style={styles.headerRow}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Text style={styles.backButtonText}>← Back</Text>
          </TouchableOpacity>
          <Text style={styles.screenTitle}>Your Plan For Today</Text>
        </View>

        <Text style={{ color: "#94a3b8" }}>
          Waiting for server plan…
        </Text>
      </ScrollView>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      
      <View style={styles.headerRow}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.screenTitle}>Your Plan For Today</Text>
      </View>

      {loading ? (
        <Text style={{ color: "#94a3b8" }}>Loading…</Text>
      ) : err ? (
        <Text style={{ color: "#fca5a5" }}>{err}</Text>
      ) : null}

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Daily Targets</Text>

        <View style={styles.statsRow}>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{plan.nutritionToday.calorieTarget}</Text>
            <Text style={styles.statLabel}>Calories</Text>
          </View>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{plan.nutritionToday.proteinTarget}g</Text>
            <Text style={styles.statLabel}>Protein</Text>
          </View>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{plan.nutritionToday.carbsTarget}g</Text>
            <Text style={styles.statLabel}>Carbs</Text>
          </View>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{plan.nutritionToday.fatTarget}g</Text>
            <Text style={styles.statLabel}>Fat</Text>
          </View>
        </View>
      </View>

<View style={styles.card}>
  <Text style={styles.cardTitle}>Actual Intake Today</Text>

  <View style={styles.statsRow}>
    <View style={styles.statBox}>
      <Text style={styles.statNumber}>{actualTotals.calories}</Text>
      <Text style={styles.statLabel}>Calories</Text>
    </View>

    <View style={styles.statBox}>
      <Text style={styles.statNumber}>{actualTotals.protein}g</Text>
      <Text style={styles.statLabel}>Protein</Text>
    </View>

    <View style={styles.statBox}>
      <Text style={styles.statNumber}>{actualTotals.carbs}g</Text>
      <Text style={styles.statLabel}>Carbs</Text>
    </View>

    <View style={styles.statBox}>
      <Text style={styles.statNumber}>{actualTotals.fat}g</Text>
      <Text style={styles.statLabel}>Fat</Text>
    </View>
  </View>
</View>

      <View style={styles.card}>
        <View style={styles.cardHeaderRow}>
          <Text style={styles.cardTitle}>Nutrition Today</Text>
          <TouchableOpacity onPress={() => router.push("/meal-plan")}>
            <Text style={styles.linkText}>See 7-day plan →</Text>
          </TouchableOpacity>
        </View>

        {plan.meals.map((m, index) => (
          <View key={index} style={styles.mealBlock}>
            <Text style={styles.mealLabel}>{m.label}</Text>
            <Text style={styles.mealName}>{m.meal.name}</Text>

            <View style={styles.macroRow}>
              <Text style={styles.macroText}>
                {m.meal.macros.calories} kcal • P {m.meal.macros.protein}g • C {m.meal.macros.carbs}g • F {m.meal.macros.fat}g
              </Text>
            </View>

            {m.meal.ingredients?.length > 0 && (
              <Text style={styles.ingredientsText}>
                {m.meal.ingredients.join(" • ")}
              </Text>
            )}

            {m.meal.instructions ? (
              <Text style={styles.instructionText}>{m.meal.instructions}</Text>
            ) : null}
          </View>
        ))}
      </View>

      <View style={styles.card}>
        <View style={styles.cardHeaderRow}>
          <Text style={styles.cardTitle}>Workout Today</Text>
          <TouchableOpacity onPress={() => router.push("/workout-plan")}>
            <Text style={styles.linkText}>See 7-day plan →</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.sectionSubtitle}>Focus</Text>
        <Text style={styles.bodyText}>{plan.workoutFocus}</Text>

        <Text style={styles.sectionSubtitle}>Details</Text>
        {plan.workoutDetails.length ? (
          plan.workoutDetails.map((line, i) => (
            <Text key={i} style={styles.bodyBullet}>• {line}</Text>
          ))
        ) : (
          <Text style={styles.bodyText}>Rest day.</Text>
        )}

        {plan.coachNote ? (
          <>
            <Text style={styles.sectionSubtitle}>Coach Note</Text>
            <Text style={styles.bodyText}>{plan.coachNote}</Text>
          </>
        ) : null}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f172a" },
  content: { paddingHorizontal: 20, paddingTop: 40, paddingBottom: 60 },

  headerRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 24,
    flexWrap: "wrap",
  },
  backButton: {
    paddingVertical: 6,
    paddingHorizontal: 10,
    backgroundColor: "#1e253a",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#2f3a5a",
    marginRight: 10,
  },
  backButtonText: { color: "#38bdf8", fontSize: 14, fontWeight: "600" },
  screenTitle: { color: "#fff", fontSize: 18, fontWeight: "700" },

  card: {
    backgroundColor: "#1e253a",
    borderRadius: 16,
    padding: 16,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: "#2f3a5a",
  },
  cardHeaderRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 12,
  },
  cardTitle: { color: "#fff", fontSize: 18, fontWeight: "700" },
  linkText: { color: "#38bdf8", fontSize: 14, fontWeight: "600" },

  statsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    flexWrap: "wrap",
    marginTop: 16,
  },
  statBox: {
    width: "23%",
    backgroundColor: "#0f172a",
    borderRadius: 12,
    paddingVertical: 12,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#2f3a5a",
    marginBottom: 8,
  },
  statNumber: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "700",
  },
  statLabel: {
    color: "#94a3b8",
    fontSize: 12,
    marginTop: 4,
  },

  mealBlock: {
    marginBottom: 16,
    backgroundColor: "#0f172a",
    borderRadius: 12,
    padding: 12,
    borderWidth: 1,
    borderColor: "#2f3a5a",
  },
  mealLabel: {
    color: "#fff",
    fontSize: 15,
    fontWeight: "700",
  },
  mealName: {
    color: "#fff",
    fontSize: 14,
    marginTop: 4,
    fontWeight: "600",
  },
  macroRow: { marginTop: 6 },
  macroText: { color: "#38bdf8", fontSize: 13 },

  ingredientsText: {
    color: "#94a3b8",
    fontSize: 13,
    marginTop: 8,
  },
  instructionText: {
    color: "#94a3b8",
    fontSize: 13,
    lineHeight: 18,
    marginTop: 10,
  },

  sectionSubtitle: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
    marginTop: 16,
    marginBottom: 8,
  },
  bodyText: {
    color: "#94a3b8",
    fontSize: 14,
    lineHeight: 20,
  },
  bodyBullet: {
    color: "#94a3b8",
    fontSize: 14,
    marginBottom: 4,
  },
});
