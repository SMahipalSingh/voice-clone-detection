import axios from "axios";

const API_BASE = "http://localhost:8000";

const client = axios.create({
  baseURL: API_BASE,
  timeout: 120000,
});

export const analyzeAudio = async (audioBlobOrFile, scenario = "General Call", customName = null) => {
  const formData = new FormData();
  const filename = customName || (audioBlobOrFile.name ? audioBlobOrFile.name : "recorded_audio.wav");
  
  formData.append("audio", audioBlobOrFile, filename);
  formData.append("scenario", scenario);

  const response = await client.post("/analyze-audio", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return response.data;
};

export const getSampleAudios = async () => {
  const response = await client.get("/sample-audios");
  return response.data;
};

export const getSampleAudioBlob = async (sampleId) => {
  const response = await client.get(`/sample-audios/${sampleId}/audio`, {
    responseType: "blob"
  });
  return response.data;
};

export const getLedger = async () => {
  const response = await client.get("/ledger");
  return response.data;
};

export const verifyLedger = async () => {
  const response = await client.get("/ledger/verify");
  return response.data;
};

export const resetLedger = async () => {
  const response = await client.post("/ledger/reset");
  return response.data;
};

export const getHistory = async (limit = 50) => {
  const response = await client.get(`/history?limit=${limit}`);
  return response.data;
};

export const clearHistory = async () => {
  try {
    const response = await client.delete("/history");
    return response.data;
  } catch {
    // Fallback to POST /history/clear if DELETE is intercepted
    const response = await client.post("/history/clear");
    return response.data;
  }
};

export const checkHealth = async () => {
  try {
    const response = await client.get("/health");
    return response.data;
  } catch (err) {
    return { status: "offline", error: err.message };
  }
};
