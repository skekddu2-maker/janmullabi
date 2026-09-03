export const config = {
    api: {
        bodyParser: {
            sizeLimit: '10mb', // 대용량 이미지도 거뜬히 받도록 제한 해제
        },
    },
};

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { prompt, image, mimeType } = req.body;
        
        const apiKey = process.env.GEMINI_API_KEY;
        if (!apiKey) {
            return res.status(500).json({ error: 'API 키가 서버에 설정되지 않았습니다.' });
        }

        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;

        let parts = [];
        if (image) {
            parts.push({
                inlineData: {
                    mimeType: mimeType || "image/jpeg",
                    data: image
                }
            });
        }
        parts.push({
            text: (prompt || "이 빈티지 아이템을 분석해주세요.") + "\n\n당신은 세계적인 빈티지 의류 및 밀리터리, 소품 전문가입니다. 업로드된 전체 옷의 실루엣, 팟팅/스티치, 원단감, 단추 및 하드웨어 등을 바탕으로 예상 연식, 브랜드/출처, 핵심 디테일 근거를 상세히 분석해주세요."
        });

        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [{ parts: parts }]
            })
        });

        const data = await response.json();

        if (data.error) {
            return res.status(500).json({ error: data.error.message });
        }

        const resultText = data.candidates?.[0]?.content?.parts?.[0]?.text || "분석 결과를 받아오지 못했습니다.";

        return res.status(200).json({ result: resultText });
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
}
