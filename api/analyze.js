module.exports = async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') return res.status(200).end();
    if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

    try {
        const { prompt, image, mimeType } = req.body;
        const apiKey = process.env.GEMINI_API_KEY;

        if (!apiKey) {
            return res.status(500).json({ error: 'GEMINI_API_KEY가 설정되지 않았습니다.' });
        }

        const apiResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [{
                    parts: [
                        ...(image ? [{ inlineData: { mimeType: mimeType || "image/jpeg", data: image } }] : []),
                        { text: (prompt || "이 아이템을 분석해주세요.") + "\n\n당신은 세계적인 빈티지 의류 및 밀리터리 전문가입니다. 업로드된 아이템의 연식, 브랜드, 디테일 근거를 상세히 분석해주세요." }
                    ]
                }]
            })
        });

        const data = await apiResponse.json();

        if (data.error) {
            return res.status(500).json({ error: data.error.message });
        }

        const text = data.candidates?.[0]?.content?.parts?.[0]?.text || "분석 결과를 가져오지 못했습니다.";
        return res.status(200).json({ result: text });

    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
};
