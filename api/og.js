import { ImageResponse } from '@vercel/og';

export const config = { runtime: 'edge' };

export default function handler() {
  return new ImageResponse(
    {
      type: 'div',
      props: {
        style: {
          width: '1200px',
          height: '630px',
          backgroundColor: '#0E0D0B',
          display: 'flex',
          flexDirection: 'column',
          padding: '72px',
          position: 'relative',
        },
        children: [
          // Amber glow top-right
          {
            type: 'div',
            props: {
              style: {
                position: 'absolute',
                top: '-100px',
                right: '-100px',
                width: '600px',
                height: '600px',
                borderRadius: '50%',
                background: 'radial-gradient(circle, rgba(193,123,63,0.18) 0%, transparent 70%)',
              },
              children: null,
            },
          },
          // Logo row
          {
            type: 'div',
            props: {
              style: {
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '48px',
              },
              children: [
                {
                  type: 'div',
                  props: {
                    style: {
                      width: '44px',
                      height: '44px',
                      borderRadius: '10px',
                      border: '1.5px solid rgba(246,242,235,0.3)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backgroundColor: 'transparent',
                    },
                    children: {
                      type: 'div',
                      props: {
                        style: {
                          width: '8px',
                          height: '8px',
                          borderRadius: '50%',
                          backgroundColor: '#C17B3F',
                        },
                        children: null,
                      },
                    },
                  },
                },
                {
                  type: 'div',
                  props: {
                    style: {
                      color: '#F6F2EB',
                      fontSize: '26px',
                      fontFamily: 'serif',
                      fontStyle: 'italic',
                      letterSpacing: '-0.5px',
                    },
                    children: 'Calling Matrix',
                  },
                },
                {
                  type: 'div',
                  props: {
                    style: {
                      marginLeft: '16px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                      padding: '5px 12px',
                      border: '1px solid #2A2620',
                      borderRadius: '999px',
                      color: '#6E685F',
                      fontSize: '11px',
                      fontFamily: 'monospace',
                      letterSpacing: '2px',
                    },
                    children: [
                      {
                        type: 'div',
                        props: {
                          style: { width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#C17B3F' },
                          children: null,
                        },
                      },
                      'LIVE · 24/7',
                    ],
                  },
                },
              ],
            },
          },
          // Headline
          {
            type: 'div',
            props: {
              style: {
                color: '#F6F2EB',
                fontSize: '84px',
                lineHeight: '1.0',
                letterSpacing: '-3px',
                fontFamily: 'serif',
                fontWeight: 400,
              },
              children: 'Never miss another',
            },
          },
          {
            type: 'div',
            props: {
              style: {
                color: '#C17B3F',
                fontSize: '84px',
                lineHeight: '1.05',
                letterSpacing: '-3px',
                fontFamily: 'serif',
                fontStyle: 'italic',
                fontWeight: 400,
                marginBottom: '32px',
              },
              children: 'service call.',
            },
          },
          // Subline
          {
            type: 'div',
            props: {
              style: {
                color: '#A6A097',
                fontSize: '21px',
                fontFamily: 'sans-serif',
                marginBottom: 'auto',
              },
              children: '24/7 AI Receptionist for HVAC, Plumbing, Electrical & Roofing businesses.',
            },
          },
          // Divider + stats
          {
            type: 'div',
            props: {
              style: {
                display: 'flex',
                gap: '64px',
                borderTop: '1px solid #2A2620',
                paddingTop: '36px',
                marginTop: '36px',
              },
              children: [
                ['100%', 'CALLS ANSWERED'],
                ['< 2s', 'PICK-UP TIME'],
                ['37%', 'MORE BOOKINGS'],
                ['48h', 'GO LIVE'],
              ].map(([num, label]) => ({
                type: 'div',
                props: {
                  style: { display: 'flex', flexDirection: 'column', gap: '6px' },
                  children: [
                    {
                      type: 'div',
                      props: {
                        style: { color: '#C17B3F', fontSize: '44px', fontFamily: 'serif', lineHeight: '1' },
                        children: num,
                      },
                    },
                    {
                      type: 'div',
                      props: {
                        style: { color: '#6E685F', fontSize: '10px', fontFamily: 'monospace', letterSpacing: '2px' },
                        children: label,
                      },
                    },
                  ],
                },
              })),
              // Domain right-aligned
            },
          },
        ],
      },
    },
    { width: 1200, height: 630 }
  );
}
