import AppleHealthKit from "./AppleHealthKit";

const startOfToday = new Date(new Date().setHours(0, 0, 0, 0)).toISOString();
const now = new Date().toISOString();

type HealthError = string | null;
type HealthResult = any;

export function getTodayActiveEnergy(): Promise<HealthResult> {
  return new Promise((resolve, reject) => {
    const options = {
      startDate: startOfToday,
      endDate: now,
    };

    AppleHealthKit.getActiveEnergyBurned(
      options,
      (err: HealthError, result: HealthResult) => {
        if (err) {
          console.log("Active Energy Error:", err);
          return reject(err);
        }
        console.log("Active Energy:", result);
        resolve(result);
      }
    );
  });
}

export function getTodayBasalEnergy(): Promise<HealthResult> {
  return new Promise((resolve, reject) => {
    const options = {
      startDate: startOfToday,
      endDate: now,
    };

    AppleHealthKit.getBasalEnergyBurned(
      options,
      (err: HealthError, result: HealthResult) => {
        if (err) {
          console.log("Basal Energy Error:", err);
          return reject(err);
        }
        console.log("Basal Energy:", result);
        resolve(result);
      }
    );
  });
}
