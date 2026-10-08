---
name: mobile-native-ui-suite
description: "Master unified Mobile & Native App UI/UX suite. Consolidates Apple Human Interface Guidelines (HIG), SwiftUI, Android Material Design 3 & Jetpack Compose, and cross-platform mobile patterns (React Native, Expo Router, Flutter)."
category: "design-and-ux"
tools:
  - react-native
  - expo
  - swiftui
---

# Mobile & Native App UI/UX Suite (Unified Master Skill)

A comprehensive framework for crafting native, fluid, touch-optimized mobile interfaces across iOS, Android, and cross-platform runtimes (React Native / Expo / Flutter).

---

## 1. Mobile Platform Selection Ladder

```
[Mobile App Design Objective]
   │
   ├──> Cross-Platform React Native / Universal App?
   │       └──> Expo Router + NativeWind (`react-native-design`, `building-native-ui`, `expo-ui`)
   │            File-based routing, native tabs, safe area insets, Reanimated gestures.
   │
   ├──> Native iOS / macOS / watchOS App?
   │       └──> Apple HIG & SwiftUI (`apple-hig`, `swiftui-design`, `swiftui-ui-patterns`)
   │            Human Interface Guidelines, Liquid Glass effects, SF Symbols, dynamic island / widgets.
   │
   ├──> Native Android App?
   │       └──> Material Design 3 & Jetpack Compose (`mobile-android-design`, `android-jetpack-compose-expert`)
   │            Material You dynamic theming, scaffold architecture, surface elevation, ripple effects.
   │
   └──> High-Performance Native Flutter?
           └──> Flutter Material/Cupertino Widgets (`flutter-expert`, `flutter-animating-apps`)
                Declarative widget tree, custom painters, sliver scroll physics.
```

---

## 2. Core Mobile UX Principles

1. **Safe Area Insets:** Always account for system status bars, notches, home indicator bars, and keyboard appearance (`useSafeAreaInsets()`, `safeAreaPadding`).
2. **Thumb Zone Ergonomics:** Primary navigation and key interactive triggers must live in the lower third of the viewport. High-risk destructive actions belong away from natural resting thumb reach.
3. **Touch Targets & Hit Slop:** Interactive elements require a minimum hit box of **44x44pt** (iOS) / **48x48dp** (Android). Use `hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}` for smaller inline icons.
4. **Haptic Feedback:** Pair meaningful gestures and state shifts with subtle haptics (impact feedback on selection, notification feedback on success/failure).

---

## 3. Expo Router & React Native Architecture Pattern

```tsx
import React from 'react';
import { View, Text, Pressable, ScrollView } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as Haptics from 'expo-haptics';

export default function MobileScreen() {
  const insets = useSafeAreaInsets();

  const handlePress = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    // Execute action
  };

  return (
    <View style={{ flex: 1, paddingTop: insets.top, paddingBottom: insets.bottom }} className="bg-slate-50 dark:bg-slate-950">
      <ScrollView contentContainerStyle={{ paddingHorizontal: 16, paddingBottom: 24 }} showsVerticalScrollIndicator={false}>
        <Text className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-50 mb-4">
          Account Overview
        </Text>
        
        {/* Native Card */}
        <View className="rounded-2xl p-4 bg-white dark:bg-slate-900 shadow-sm border border-slate-200/60 dark:border-slate-800">
          <Text className="text-sm font-medium text-slate-500">Balance</Text>
          <Text className="text-3xl font-extrabold text-slate-900 dark:text-slate-50 mt-1">$12,450.00</Text>
        </View>

        {/* Primary Action Button */}
        <Pressable
          onPress={handlePress}
          className="mt-6 rounded-xl bg-blue-600 active:bg-blue-700 py-3.5 items-center justify-center shadow-md active:scale-[0.98] transition-transform"
        >
          <Text className="text-base font-semibold text-white">Transfer Funds</Text>
        </Pressable>
      </ScrollView>
    </View>
  );
}
```

---

## 4. Apple HIG vs. Material Design 3 Cheat Sheet

| Design Dimension | Apple Human Interface Guidelines (HIG) | Material Design 3 (Android) |
| :--- | :--- | :--- |
| **Primary Typography** | SF Pro (System font, tight tracking) | Roboto / Dynamic Roboto Flex |
| **Bottom Navigation** | Tab Bar with SF Symbols (3–5 tabs) | Navigation Bar with pill indicators |
| **Surface Separation** | Grouped table styling, translucency, hairline borders | Tonal surface elevation, subtle shadows |
| **Back Navigation** | Interactive edge-swipe gesture + Left Chevron | System Predictive Back Gesture + Back button |
| **Action Confirmation** | Action Sheet (bottom slide-up sheet) | Modal Bottom Sheet or Dialog |

---

## 5. Mobile UI Quality Checklist

- [ ] Interface runs cleanly on both light and dark system appearances.
- [ ] Keyboard handling configured with `KeyboardAvoidingView` or `KeyboardAwareScrollView`.
- [ ] List performance optimized using `FlashList` or properly memoized `FlatList`.
- [ ] Touch feedback immediate (< 100ms) with native opacity, ripple, or scale animations.
