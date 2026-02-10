import { router } from "expo-router";
import React, { useEffect, useMemo, useState } from "react";
import {
  ActivityIndicator,
  ScrollView,
  Share,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

import { api } from "./lib/api";
import { getUserId } from "./lib/storage";

export default function GroceryListScreen() {
  const [items, setItems] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const uid = await getUserId();
        if (!uid) throw new Error("Missing userId");
        const res = await api.getCurrentPlan(uid);
        const gl = Array.isArray(res?.grocery_list) ? res.grocery_list : [];
        if (mounted) setItems(gl.map((x: any) => String(x)));
      } catch (e: any) {
        if (mounted) setErr(e?.message || "Failed to load grocery list.");
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);

  const shareText = useMemo(() => {
    if (!items.length) return "Grocery List is empty.";
    return `Grocery List\n\n${items.map((i) => `• ${i}`).join("\n")}\n`;
  }, [items]);

  async function handleShare() {
    try {
      await Share.share({ message: shareText });
    } catch {
    }
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.headerRow}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>

        <Text style={styles.title}>Grocery List</Text>

        <TouchableOpacity onPress={handleShare} style={styles.actionLink}>
          <Text style={styles.linkText}>Share / Download →</Text>
        </TouchableOpacity>
      </View>

      {loading ? (
        <View style={styles.loadingBox}>
          <ActivityIndicator />
          <Text style={styles.loadingText}>Fetching your grocery list…</Text>
        </View>
      ) : err ? (
        <Text style={styles.errorText}>{err}</Text>
      ) : items.length === 0 ? (
        <Text style={styles.emptyText}>
          No grocery items yet. Generate a plan from Food Preferences first.
        </Text>
      ) : (
        <View style={styles.card}>
          {items.map((it, idx) => (
            <View key={`${it}-${idx}`} style={styles.itemRow}>
              <Text style={styles.bullet}>•</Text>
              <Text style={styles.itemText}>{it}</Text>
            </View>
          ))}
        </View>
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

  itemRow: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: 8,
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#2f3a5a",
  },
  bullet: { color: "#94a3b8", fontSize: 16, lineHeight: 22, marginTop: 1 },
  itemText: { color: "#fff", fontSize: 14, lineHeight: 20 },
});
