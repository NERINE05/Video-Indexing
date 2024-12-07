const { VideoIntelligenceServiceClient } = require('@google-cloud/video-intelligence');
const client = new VideoIntelligenceServiceClient();

async function annoteVideo(){
  const videoContext = {
      speechTranscriptionConfig: {
        languageCode: 'en-US',
        enableAutomaticPunctuation: true,
      },
    };
    
    const request = {
      inputUri: `gs://my-video-bucket05/This student short film got me into 10 film festivals (Shot on Fuji XT4).mp4`, // Replace with your video gs:// path
      outputUri: `gs://my-video-bucket_output05/results4.json`, // Replace with your output bucket
      features: [
        'LABEL_DETECTION',
        'SHOT_CHANGE_DETECTION',
        'TEXT_DETECTION',
        'SPEECH_TRANSCRIPTION'
      ],
      videoContext: videoContext,
    };
    try {
      const [operation] = await client.annotateVideo(request);
      console.log('Waiting for operation to complete...');
      const [response] = await operation.promise();
      console.log('Video annotations:', response);
  } catch (error) {
      console.error('Error during annotation:', error);
  }
  console.log('Video analysis completed successfully!');
}
  
 annoteVideo(); 
  