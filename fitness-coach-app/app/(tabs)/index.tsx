import { router } from "expo-router";
import React, { useState } from "react";
import {
  FlatList,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function ProfileSetupScreen() {
  const [age, setAge] = useState("");
  const [heightCm, setHeightCm] = useState("");
  const [weightKg, setWeightKg] = useState("");

  const [sex, setSex] = useState<null | string>(null);
  const [activity, setActivity] = useState<null | string>(null);
  const [goal, setGoal] = useState<null | string>(null);

  const [openSelect, setOpenSelect] = useState<null | "sex" | "activity" | "goal">(null);

  const sexOptions = ["Male", "Female"];
  const activityOptions = ["Sedentary", "Light", "Moderate", "Intense"];
  const goalOptions = ["Lose Fat", "Build Muscle", "Maintain"]; // <-- was missing before

  const GOAL_VALUE_BY_LABEL: Record<string, string> = {
    "Build Muscle": "muscle_gain",
    "Lose Fat": "fat_loss",
    "Maintain": "recomp",
  };

  const handleContinue = () => {
    const goalValue = goal ? GOAL_VALUE_BY_LABEL[goal] ?? "" : "";

    console.log("NAV → /food-prefs params", {
      age, sex, heightCm, weightKg, activity, goalValue
    });

    router.push({
      pathname: "/food-prefs",
      params: {
        age,
        sex: sex ?? "",
        heightCm,
        weightKg,
        activity: activity ?? "",
        goal: goalValue,
      },
    });
  };

  const renderDropdown = (type: "sex" | "activity" | "goal") => {
    let data: string[] = [];
    let setter: (val: string) => void;

    if (type === "sex") {
      data = sexOptions;
      setter = setSex;
    } else if (type === "activity") {
      data = activityOptions;
      setter = setActivity;
    } else {
      data = goalOptions;
      setter = setGoal;
    }

    if (openSelect !== type) return null;

    return (
      <View style={styles.dropdown}>
        <FlatList
          data={data}
          keyExtractor={(item) => item}
          renderItem={({ item }) => (
            <Pressable
              style={styles.dropdownItem}
              onPress={() => {
                setter(item);
                setOpenSelect(null);
              }}
            >
              <Text style={styles.dropdownText}>{item}</Text>
            </Pressable>
          )}
        />
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView style={styles.container} contentContainerStyle={styles.inner}>
        <Text style={styles.header}>Tell me about you</Text>

        {/* Age */}
        <Text style={styles.label}>Age</Text>
        <TextInput
          style={styles.input}
          placeholder="e.g. 29"
          placeholderTextColor="#94a3b8"
          value={age}
          onChangeText={setAge}
          keyboardType="numeric"
        />

        {/* Sex */}
        <Text style={styles.label}>Sex</Text>
        <Pressable
          style={styles.selectBox}
          onPress={() => setOpenSelect(openSelect === "sex" ? null : "sex")}
        >
          <Text style={sex ? styles.selectValue : styles.selectPlaceholder}>
            {sex || "Select your gender"}
          </Text>
        </Pressable>
        {renderDropdown("sex")}

        {/* Height */}
        <Text style={styles.label}>Height (cm)</Text>
        <TextInput
          style={styles.input}
          placeholder="e.g. 165"
          placeholderTextColor="#94a3b8"
          value={heightCm}
          onChangeText={setHeightCm}
          keyboardType="numeric"
        />

        {/* Weight */}
        <Text style={styles.label}>Weight (kg)</Text>
        <TextInput
          style={styles.input}
          placeholder="e.g. 70"
          placeholderTextColor="#94a3b8"
          value={weightKg}
          onChangeText={setWeightKg}
          keyboardType="numeric"
        />

        {/* Activity */}
        <Text style={styles.label}>Activity Level</Text>
        <Pressable
          style={styles.selectBox}
          onPress={() => setOpenSelect(openSelect === "activity" ? null : "activity")}
        >
          <Text style={activity ? styles.selectValue : styles.selectPlaceholder}>
            {activity || "Select your activity level"}
          </Text>
        </Pressable>
        {renderDropdown("activity")}

        {/* Goal */}
        <Text style={styles.label}>Goal</Text>
        <Pressable
          style={styles.selectBox}
          onPress={() => setOpenSelect(openSelect === "goal" ? null : "goal")}
        >
          <Text style={goal ? styles.selectValue : styles.selectPlaceholder}>
            {goal || "Select your goal"}
          </Text>
        </Pressable>
        {renderDropdown("goal")}

        {/* Continue */}
        <TouchableOpacity style={styles.button} onPress={handleContinue}>
          <Text style={styles.buttonText}>Continue →</Text>
        </TouchableOpacity>

        <View style={{ height: 80 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const commonFieldBase = {
  backgroundColor: "#334155",
  borderRadius: 10,
  paddingHorizontal: 12,
  paddingVertical: 14,
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: "#1e293b" },
  container: { backgroundColor: "#1e293b", flex: 1 },
  inner: { padding: 24, paddingBottom: 60 },
  header: { color: "#fff", fontSize: 26, fontWeight: "700", marginBottom: 24 },
  label: { color: "#fff", fontSize: 14, fontWeight: "500", marginTop: 16, marginBottom: 6 },
  input: { ...commonFieldBase, color: "#fff", fontSize: 16 },
  selectBox: { ...commonFieldBase, flexDirection: "row", alignItems: "center", justifyContent: "space-between" },
  selectValue: { color: "#fff", fontSize: 16 },
  selectPlaceholder: { color: "#94a3b8", fontSize: 16, fontStyle: "italic" },
  dropdown: { backgroundColor: "#1e293b", borderWidth: 1, borderColor: "#475569", borderRadius: 10, marginTop: 8, overflow: "hidden" },
  dropdownItem: { paddingVertical: 14, paddingHorizontal: 16, borderBottomWidth: 1, borderBottomColor: "#334155" },
  dropdownText: { color: "#fff", fontSize: 16 },
  button: { backgroundColor: "#38bdf8", paddingVertical: 16, borderRadius: 12, alignItems: "center", justifyContent: "center", marginTop: 32 },
  buttonText: { color: "#0f172a", fontSize: 16, fontWeight: "600" },
});
