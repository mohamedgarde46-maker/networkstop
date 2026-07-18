const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

let activeProcesses = [];

// إعدادات كارت الشبكة والـ Gateway الخاصة بك
const INTERFACE = 'wlan0'; 
const GATEWAY = '192.168.0.1'; // تم التحديث بناءً على رينج الـ IP لديك 192.168.0.x

// --- 1. هێرشکردنە سەر هەموو ئامێرەکان (Isolate All) ---
app.post('/api/network/isolate-all', (req, res) => {
    if (activeProcesses.length > 0) {
        return res.json({ success: true, message: 'هێرشەکە پێشتر چالاک کراوە!' });
    }

    console.log(`[+] جاری دەستپێکردنی عەزلکردنی گشتی لەسەر تەواوی تۆڕەکە...`);

    // بەکارهێنانی نیشانەی گشتی بۆ عەزلکردنی هەموو ئامێرەکانی ناو ڕاوتەرەکە بە یەک فەرمان
    const command = `sudo arpspoof -i ${INTERFACE} ${GATEWAY}`;
    
    const childProcess = exec(command, (error) => {
        if (error && !error.killed) console.error(`[-] خەتا لە جێبەجێکردندا: ${error.message}`);
    });

    activeProcesses.push(childProcess);

    res.json({
        success: true,
        message: 'ئینتەرنێت لەسەر تەواوی ئامێرەکانی تۆڕەکە بڕدرا! 🚫'
    });
});

// --- 2. هێنانەوەی هێڵ بۆ هەمووان (Restore All) ---
app.post('/api/network/restore-all', (req, res) => {
    if (activeProcesses.length > 0) {
        activeProcesses.forEach(proc => proc.kill('SIGINT'));
        activeProcesses = [];
        console.log(`[+] هێرشەکە ڕاگیرا و ئینتەرنێت بۆ هەمووان گەڕایەوە.`);
        return res.json({ success: true, message: 'هێڵ بۆ تەواوی ئامێرەکان گەڕایەوە بنەچەی خۆی. ✅' });
    } else {
        return res.status(404).json({ success: false, error: 'هیچ هێرشێکی گشتی چالاک نییە کاتی ئێستا!' });
    }
});

app.listen(PORT, () => {
    console.log(`====== NetStop Tool Ready ======`);
    console.log(`[+] Server running on: http://localhost:${PORT}`);
});