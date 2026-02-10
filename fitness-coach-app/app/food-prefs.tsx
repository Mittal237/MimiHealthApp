import { router, useLocalSearchParams } from "expo-router";
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
import { requestHealthPermissions } from "./lib/apple/appleHealthPermissions";
import { getUserId, saveUserId } from "./lib/storage";


const takeFirst = (v?: string | string[]) =>
  Array.isArray(v) ? (v[0] ?? "") : (v ?? "");

const firstToken = (s: string) => s.split(",")[0].trim(); 

const GOAL_BY_LABEL: Record<string, string> = {
  "Build Muscle": "muscle_gain",
  "Lose Fat": "fat_loss",
  "Maintain": "recomp",
  "Loose Felt": "fat_loss", 
};

const ACTIVITY_BY_LABEL: Record<string, string> = {
  "Sedentary": "sedentary",
  "Light": "light",
  "Moderate": "moderate",
  "Intense": "intense",
};

export default function FoodPrefsScreen() {
  const params = useLocalSearchParams<{
    age?: string | string[];
    sex?: string | string[];
    heightCm?: string | string[];
    weightKg?: string | string[];
    activity?: string | string[]; 
    goal?: string | string[];     
  }>();

  const age      = takeFirst(params.age);
  const sex      = takeFirst(params.sex);
  const heightCm = takeFirst(params.heightCm);
  const weightKg = takeFirst(params.weightKg);
 
  const rawActivity = firstToken(takeFirst(params.activity)); 
  const rawGoal     = firstToken(takeFirst(params.goal));     

  const activityCanonical = ACTIVITY_BY_LABEL[rawActivity] ?? rawActivity; 
  const goalCanonical     = GOAL_BY_LABEL[rawGoal] ?? rawGoal;             

  const [dietType, setDietType] = useState<"veg" | "nonveg">("nonveg");
  const [favProtein, setFavProtein] = useState<string>("chicken breast");

  const [submitting, setSubmitting] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    console.log("FOOD-PREFS PARAMS →", params);
    console.log("NORMALIZED →", { goalCanonical, activityCanonical });
  }, [params]);

  async function handleGeneratePlan() {
    setSubmitting(true);
    setErr(null);

    try {
      try {
        await requestHealthPermissions();
        console.log("HealthKit permissions granted");
      } 
      catch (hkErr) {
        console.log("HealthKit permission failed:", hkErr);
      }
      
      const existing = await getUserId(); 
      let userId: string;

      if (existing) {
        userId = existing; 
      } else {
        const signupRes = await api.signup({
          first_name: "Test",
          last_name: "User",
          email: `user${Date.now()}@example.com`,
          password: "secret",
        });
        userId = signupRes.userId; 
        await saveUserId(userId); 
      }

      await api.setupProfile({
        user_id: userId,
        age: age ? Number(age) : null,
        sex: sex || null,
        height_cm: heightCm ? Number(heightCm) : null,
        weight_kg: weightKg ? Number(weightKg) : null,
        activity_level: activityCanonical || null,  
        goal: goalCanonical || null,               
        diet_type: dietType,
        fav_protein: favProtein,
        experience_level: "intermediate", 
      });

      await api.generateWeek(userId);

      router.push("/plan");
    } catch (e: any) {
      setErr(e?.message || "Failed to create your plan. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <View style={styles.headerRow}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => router.back()}
          disabled={submitting}
        >
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>

        <View style={{ flex: 1 }}>
          <Text style={styles.headerTitle}>Food Preferences</Text>
          <Text style={styles.headerSub}>
            We'll build meals and your grocery list based on this.
          </Text>
        </View>
      </View>

      {err ? <Text style={styles.errorText}>{err}</Text> : null}

      <View style={styles.card}>
        <Text style={styles.cardLabel}>Diet style</Text>

        <View style={styles.rowWrap}>
          <TouchableOpacity
            style={[styles.chip, dietType === "veg" && styles.chipActive]}
            onPress={() => {
              setDietType("veg");
              setFavProtein("tofu");
            }}
            disabled={submitting}
          >
            <Text
              style={[styles.chipText, dietType === "veg" && styles.chipTextActive]}
            >
              Vegetarian
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.chip, dietType === "nonveg" && styles.chipActive]}
            onPress={() => {
              setDietType("nonveg");
              setFavProtein("chicken breast");
            }}
            disabled={submitting}
          >
            <Text
              style={[styles.chipText, dietType === "nonveg" && styles.chipTextActive]}
            >
              Non-Veg
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardLabel}>Favorite protein source</Text>
        <Text style={styles.currentChoiceValue}>{favProtein}</Text>

        <View style={styles.rowWrap}>
          {dietType === "veg" ? (
            <>
              <TouchableOpacity
                style={styles.proteinChoice}
                onPress={() => setFavProtein("tofu")}
                disabled={submitting}
              >
                <Text style={styles.proteinChoiceText}>Tofu</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.proteinChoice}
                onPress={() => setFavProtein("paneer")}
                disabled={submitting}
              >
                <Text style={styles.proteinChoiceText}>Paneer</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.proteinChoice}
                onPress={() => setFavProtein("eggs")}
                disabled={submitting}
              >
                <Text style={styles.proteinChoiceText}>Eggs</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.proteinChoice}
                onPress={() => setFavProtein("greek yogurt")}
                disabled={submitting}
              >
                <Text style={styles.proteinChoiceText}>Greek yogurt</Text>
              </TouchableOpacity>
            </>
          ) : (
            <>
              <TouchableOpacity
                style={styles.proteinChoice}
                onPress={() => setFavProtein("chicken breast")}
                disabled={submitting}
              >
                <Text style={styles.proteinChoiceText}>Chicken</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.proteinChoice}
                onPress={() => setFavProtein("salmon")}
                disabled={submitting}
              >
                <Text style={styles.proteinChoiceText}>Salmon</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.proteinChoice}
                onPress={() => setFavProtein("turkey")}
                disabled={submitting}
              >
                <Text style={styles.proteinChoiceText}>Turkey</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.proteinChoice}
                onPress={() => setFavProtein("eggs")}
                disabled={submitting}
              >
                <Text style={styles.proteinChoiceText}>Eggs</Text>
              </TouchableOpacity>
            </>
          )}
        </View>
      </View>

      <TouchableOpacity
        style={[styles.primaryButton, submitting && { opacity: 0.7 }]}
        onPress={handleGeneratePlan}
        disabled={submitting}
      >
        {submitting ? (
          <View style={{ flexDirection: "row", alignItems: "center", gap: 8 }}>
            <ActivityIndicator color="#0f172a" />
            <Text style={styles.primaryButtonText}>Building your plan…</Text>
          </View>
        ) : (
          <Text style={styles.primaryButtonText}>Generate My Plan →</Text>
        )}
      </TouchableOpacity>

      <View style={{ height: 80 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: "#0f172a",
  },
  container: {
    paddingHorizontal: 20,
    paddingTop: 32,
    paddingBottom: 40,
  },

  headerRow: {
    flexDirection: "row",
    alignItems: "flex-start",
    marginBottom: 28,
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
  backButtonText: {
    color: "#38bdf8",
    fontSize: 14,
    fontWeight: "600",
  },
  headerTitle: {
    color: "#fff",
    fontSize: 20,
    fontWeight: "700",
    marginBottom: 6,
  },
  headerSub: {
    color: "#94a3b8",
    fontSize: 14,
    lineHeight: 20,
  },

  errorText: {
    color: "#fca5a5",
    marginBottom: 12,
    fontSize: 14,
  },

  card: {
    backgroundColor: "#1e253a",
    borderRadius: 16,
    padding: 16,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: "#2f3a5a",
  },

  cardLabel: {
    color: "#fff",
    fontSize: 14,
    fontWeight: "600",
    marginBottom: 12,
  },

  currentChoiceValue: {
    color: "#38bdf8",
    fontSize: 14,
    fontWeight: "600",
    marginBottom: 12,
  },

  rowWrap: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
  },

  chip: {
    backgroundColor: "#0f172a",
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#2f3a5a",
    paddingVertical: 10,
    paddingHorizontal: 12,
  },
  chipActive: {
    backgroundColor: "#38bdf8",
    borderColor: "#38bdf8",
  },
  chipText: {
    color: "#94a3b8",
    fontSize: 14,
    fontWeight: "600",
  },
  chipTextActive: {
    color: "#0f172a",
    fontSize: 14,
    fontWeight: "600",
  },

  proteinChoice: {
    backgroundColor: "#0f172a",
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#2f3a5a",
    paddingVertical: 8,
    paddingHorizontal: 12,
  },
  proteinChoiceText: {
    color: "#fff",
    fontSize: 13,
    fontWeight: "500",
  },

  primaryButton: {
    backgroundColor: "#38bdf8",
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#38bdf8",
    marginTop: 8,
  },
  primaryButtonText: {
    color: "#0f172a",
    fontSize: 16,
    fontWeight: "700",
  },
});
