import AppleHealthKit from "./AppleHealthKit";

export async function requestHealthPermissions() {
  const permissions = {
    permissions: {
      read: [
        AppleHealthKit.Constants.Permissions.ActiveEnergyBurned,
        AppleHealthKit.Constants.Permissions.BasalEnergyBurned,
        AppleHealthKit.Constants.Permissions.Steps,
        AppleHealthKit.Constants.Permissions.HeartRate,
        AppleHealthKit.Constants.Permissions.Workout,
      ],
      write: [],
    },
  };

  return new Promise((resolve, reject) => {
    AppleHealthKit.initHealthKit(permissions, (err: any) => {
      if (err) {
        console.log("HealthKit Authorization ERROR:", err);
        reject(err);
      } else {
        console.log("HealthKit Authorization SUCCESS!");
        resolve(true);
      }
    });
  });
}
