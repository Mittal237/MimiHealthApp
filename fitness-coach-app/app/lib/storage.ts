import AsyncStorage from "@react-native-async-storage/async-storage";

const USER_KEY = "userId";

export async function saveUserId(id: string) {
  await AsyncStorage.setItem(USER_KEY, id);
}

export async function getUserId() {
  return AsyncStorage.getItem(USER_KEY);
}
