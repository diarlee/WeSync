'use client';

// import React, { useEffect, useRef, useState } from 'react';
import React, { useEffect, useRef } from 'react';
import { useSingleAudioStore } from '@/store/singleAudioStore';
import AudioPlayer from 'react-h5-audio-player';
import 'react-h5-audio-player/lib/styles.css';
import { useMultiAudioStore } from '@/store/multiAudioStore';

export default function FixedAudioPlayer() {
  const { currentTrackUrl, currentId, playing, stopTrack } = useSingleAudioStore();
  const { isPlaying } = useMultiAudioStore();
  const audioRef = useRef<AudioPlayer>(null);
  //   const [initialVolume, setInitialVolume] = useState<number>(0.3); // 기본 볼륨 상태

  useEffect(() => {
    if (audioRef.current && audioRef.current.audio.current) {
      if (currentId === 1) {
        audioRef.current.audio.current.volume = 0.2; // currentId가 1일 때 볼륨 0.5
      } else {
        audioRef.current.audio.current.volume = 0.3; // 그 외에는 기본 볼륨
      }
    }
  }, [currentId]); // currentId가 변경될 때만 볼륨 상태 업데이트

  useEffect(() => {
    if (audioRef.current && audioRef.current.audio.current) {
      if (playing) {
        audioRef.current.audio.current.play();
      } else {
        audioRef.current.audio.current.pause();
      }
    }
  }, [playing]); // playing이 변경될 때만 재생 상태 업데이트

  return (
    <>
      {isPlaying === false && (
        <div
          style={{
            position: 'fixed',
            bottom: 0,
            left: 0,
            width: '100%',
            height: '14vh',
            minHeight: '100px',
          }}
        >
          <AudioPlayer
            src={currentTrackUrl}
            autoPlay={playing}
            // header={playing.toString()}
            onPause={stopTrack}
            preload="auto"
            ref={audioRef}
            // onPlay={() => console.log('Playing with ID:', currentId)}
            style={{ height: '100%', zIndex: 1000, display: 'block' }}
          />
        </div>
      )}
    </>
  );
}
