export async function getInvestigationData() {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
    })
  
    if (!response.ok) {
      throw new Error("Failed to fetch data")
    }
  
    return response.json()
  }
  