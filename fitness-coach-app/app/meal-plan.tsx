import { router } from "expo-router";
import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

import { api } from "./lib/api";
import { getUserId } from "./lib/storage";

type MealEntry = {
  label: string; 
  meal: {
    name: string;
    macros: { calories: number; protein: number; carbs: number; fat: number };
    ingredients?: string[];
    instructions?: string;
    tags?: string[];
  };
};

type DayMeals = { day: string; meals: MealEntry[] };

const DAY_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"] as const;

export default function MealPlanScreen() {
  const [weekMeals, setWeekMeals] = useState<DayMeals[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    (async () => {
      try {
        const uid = await getUserId();
        if (!uid) throw new Error("Missing userId");

        const res = await api.getCurrentPlan(uid);

        const wm = res?.week_meals ?? null;

        const mapped: DayMeals[] = wm
          ? DAY_KEYS.map((k, i) => ({
              day: `Day ${i + 1}`,
              meals: Array.isArray(wm[k]) ? wm[k] : [],
            }))
          : [];

        if (mounted) setWeekMeals(mapped);
      } catch (e: any) {
        if (mounted) setErr(e?.message || "Failed to load meal plan.");
      } finally {
        if (mounted) setLoading(false);
      }
    })();

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.headerRow}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>

        <Text style={styles.title}>7-Day Meal Plan</Text>

        <TouchableOpacity
          onPress={() => router.push("/grocery-list")}
          style={styles.actionLink}
        >
          <Text style={styles.linkText}>View Grocery List →</Text>
        </TouchableOpacity>
      </View>

      {loading ? (
        <View style={styles.loadingBox}>
          <ActivityIndicator />
          <Text style={styles.loadingText}>Loading your meals…</Text>
        </View>
      ) : err ? (
        <Text style={styles.errorText}>{err}</Text>
      ) : weekMeals.length === 0 ? (
        <Text style={styles.emptyText}>No meal plan found for this week.</Text>
      ) : (
        weekMeals.map((d, idx) => (
          <View key={idx} style={styles.card}>
            <View style={styles.cardHeader}>
              <Text style={styles.cardTitle}>{d.day}</Text>
            </View>

            {d.meals.length === 0 ? (
              <Text style={styles.bodyText}>No meals added for this day.</Text>
            ) : (
              d.meals.map((entry, i) => {
                const m = entry.meal;
                return (
                  <View key={i} style={styles.mealBlock}>
                    <Text style={styles.mealLabel}>{entry.label}</Text>
                    <Text style={styles.mealName}>{m.name}</Text>

                    <View style={styles.macrosRow}>
                      <Text style={styles.macroText}>
                        {m.macros.calories} kcal
                      </Text>
                      <Text style={styles.macroText}>
                        P:{m.macros.protein}g
                      </Text>
                      <Text style={styles.macroText}>
                        C:{m.macros.carbs}g
                      </Text>
                      <Text style={styles.macroText}>
                        F:{m.macros.fat}g
                      </Text>
                    </View>

                    {m.ingredients && m.ingredients.length > 0 && (
                      <View style={{ marginTop: 6 }}>
                        <Text style={styles.sectionTitle}>Ingredients</Text>
                        {m.ingredients.map((ing, idx2) => (
                          <Text key={idx2} style={styles.ingredientText}>
                            • {ing}
                          </Text>
                        ))}
                      </View>
                    )}

                    {m.instructions ? (
                      <View style={{ marginTop: 8 }}>
                        <Text style={styles.sectionTitle}>Instructions</Text>
                        <Text style={styles.instructionsText}>
                          {m.instructions}
                        </Text>
                      </View>
                    ) : null}
                  </View>
                );
              })
            )}
          </View>
        ))
      )}

      <View style={{ height: 60 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f172a" },
  content: { paddingHorizontal: 20, paddingTop: 28, paddingBottom: 40 },

  headerRow: { gap: 12, marginBottom: 16 },
  backButton: {
    alignSelf: "flex-start",
    paddingVertical: 6,
    paddingHorizontal: 10,
    backgroundColor: "#1e253a",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#2f3a5a",
  },
  backButtonText: { color: "#38bdf8", fontSize: 14, fontWeight: "600" },
  title: { color: "#fff", fontSize: 20, fontWeight: "700", marginTop: 4 },
  actionLink: { marginTop: 8, alignSelf: "flex-start" },
  linkText: { color: "#38bdf8", fontSize: 14, fontWeight: "600" },

  loadingBox: {
    marginTop: 12,
    padding: 16,
    backgroundColor: "#1e253a",
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#2f3a5a",
    alignItems: "center",
  },
  loadingText: { color: "#94a3b8", marginTop: 8 },

  errorText: { color: "#fca5a5", marginTop: 8 },
  emptyText: { color: "#94a3b8", marginTop: 8 },

  card: {
    backgroundColor: "#1e253a",
    borderRadius: 16,
    padding: 16,
    marginTop: 16,
    borderWidth: 1,
    borderColor: "#2f3a5a",
  },
  cardHeader: { marginBottom: 8 },
  cardTitle: { color: "#fff", fontSize: 16, fontWeight: "700" },

  mealBlock: {
    marginTop: 12,
    backgroundColor: "#0f172a",
    borderRadius: 12,
    padding: 12,
    borderWidth: 1,
    borderColor: "#2f3a5a",
  },

  mealLabel: { color: "#38bdf8", fontSize: 14, fontWeight: "700" },
  mealName: { color: "#fff", fontSize: 15, fontWeight: "600", marginTop: 2 },

  macrosRow: {
    flexDirection: "row",
    gap: 12,
    marginTop: 6,
  },
  macroText: { color: "#94a3b8", fontSize: 13, fontWeight: "600" },

  sectionTitle: {
    color: "#cbd5e1",
    fontSize: 13,
    fontWeight: "600",
    marginBottom: 2,
  },
  ingredientText: { color: "#94a3b8", fontSize: 13, marginLeft: 4 },
  instructionsText: { color: "#94a3b8", fontSize: 13, marginTop: 2 },

  bodyText: { color: "#94a3b8", fontSize: 14, lineHeight: 20 },
});
