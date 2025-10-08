<?php
header('Content-Type: application/json');
$input = json_decode(file_get_contents('php://input'), true);
$message = $input['message'] ?? '';

$apiKey = "YOUR_OPENAI_API_KEY"; // replace with your key

$data = [
    "model" => "gpt-3.5-turbo",
    "messages" => [["role"=>"user","content"=>$message]]
];

$ch = curl_init("https://api.openai.com/v1/chat/completions");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
  "Content-Type: application/json",
  "Authorization: Bearer $apiKey"
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
$response = curl_exec($ch);
curl_close($ch);

$resData = json_decode($response,true);
$reply = $resData['choices'][0]['message']['content'] ?? "Sorry, I didn't get that.";

echo json_encode(['reply'=>$reply]);
?>
