import { router } from "expo-router";
import React, { useEffect, useState } from "react";
import { ScrollView, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { api } from "./lib/api";
import { getUserId } from "./lib/storage";

type WorkoutItem = { name: string; sets?: number; reps?: string; time?: string };
type WorkoutDay = { focus: string; details: WorkoutItem[]; coachNote?: string };
type WeekWorkouts = { mon: WorkoutDay; tue: WorkoutDay; wed: WorkoutDay; thu: WorkoutDay; fri: WorkoutDay; sat: WorkoutDay; sun: WorkoutDay };

const fmt = (ex: WorkoutItem) => {
  if (ex.time) return `${ex.name} — ${ex.time}`;
  if (ex.sets && ex.reps) return `${ex.name} — ${ex.sets} × ${ex.reps}`;
  if (ex.sets) return `${ex.name} — ${ex.sets} sets`;
  return ex.name;
};

export default function WorkoutPlanScreen() {
  const [week, setWeek] = useState<WeekWorkouts | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const id = await getUserId();
         if (!id) {
        setErr("Missing user ID");
        setLoading(false);
        return;
      }

        console.log("WorkoutPlan → userId:", id);
        const res = await api.getCurrentPlan(id);
        console.log("WorkoutPlan getCurrentPlan() →", res);
        setWeek(res.week_workouts);
      } catch (e: any) {
        console.error("WorkoutPlan fetch error:", e);
        setErr(e?.message || "Failed to load workouts");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const order: (keyof WeekWorkouts)[] = ["mon","tue","wed","thu","fri","sat","sun"];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.topRow}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.screenTitle}>7-Day Workout Plan</Text>
      </View>

      {loading && <Text style={styles.loading}>Loading…</Text>}
      {err && <Text style={styles.error}>{err}</Text>}
      {!week && !loading && !err && <Text style={styles.loading}>No workouts available.</Text>}

      {week &&
        order.map((k, i) => {
          const d = week[k];
          const isRest = !d?.details?.length;
          return (
            <View key={k} style={styles.dayCard}>
              <Text style={styles.dayTitle}>Day {i + 1}</Text>

              <Text style={styles.sectionLabel}>Focus</Text>
              <Text style={styles.bodyText}>{d?.focus || (isRest ? "Rest Day" : "")}</Text>

              {isRest ? (
                <Text style={styles.bodyText}>Rest — recover.</Text>
              ) : (
                <>
                  <Text style={styles.sectionLabel}>Workout</Text>
                  {d.details.map((ex, j) => (
                    <Text key={j} style={styles.bodyBullet}>
                      • {fmt(ex)}
                    </Text>
                  ))}
                </>
              )}

              {!!d?.coachNote && (
                <>
                  <Text style={styles.sectionLabel}>Note</Text>
                  <Text style={styles.bodyText}>{d.coachNote}</Text>
                </>
              )}
            </View>
          );
        })}
      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f172a" },
  content: { paddingHorizontal: 20, paddingTop: 40, paddingBottom: 60 },
  topRow: {
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
  dayCard: {
    backgroundColor: "#1e253a",
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#2f3a5a",
    padding: 16,
    marginBottom: 20,
  },
  dayTitle: { color: "#fff", fontSize: 16, fontWeight: "700", marginBottom: 12 },
  sectionLabel: {
    color: "#fff",
    fontSize: 15,
    fontWeight: "600",
    marginTop: 8,
    marginBottom: 4,
  },
  bodyText: { color: "#94a3b8", fontSize: 14, lineHeight: 20 },
  bodyBullet: {
    color: "#94a3b8",
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 4,
  },
  loading: { color: "#94a3b8", fontSize: 14, marginTop: 20 },
  error: { color: "#fca5a5", fontSize: 14, marginTop: 20 },
});
