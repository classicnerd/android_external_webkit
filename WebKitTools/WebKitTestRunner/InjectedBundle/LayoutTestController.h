/*
 * Copyright (C) 2010 Apple Inc. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY APPLE INC. AND ITS CONTRIBUTORS ``AS IS''
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL APPLE INC. OR ITS CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef LayoutTestController_h
#define LayoutTestController_h

#include "JSWrappable.h"
#include <JavaScriptCore/JavaScriptCore.h>
#include <wtf/PassRefPtr.h>
#include <wtf/RetainPtr.h>
#include <string>

namespace WTR {

class LayoutTestController : public JSWrappable {
public:
    static PassRefPtr<LayoutTestController> create(const std::string& testPathOrURL);
    ~LayoutTestController();

    // JSWrappable
    JSClassRef wrapperClass();

    void makeWindowObject(JSContextRef context, JSObjectRef windowObject, JSValueRef* exception);

    bool shouldDumpAsText() const { return m_dumpAsText; }
    void dumpAsText() { m_dumpAsText = true; }

    bool shouldDumpStatusCallbacks() const { return m_dumpStatusCallbacks; }
    void dumpStatusCallbacks() { m_dumpStatusCallbacks = true; }

    bool waitToDump() const { return m_waitToDump; }
    void waitToDumpWatchdogTimerFired();
    void invalidateWaitToDumpWatchdog();
    void waitUntilDone();
    void notifyDone();

    void testRepaint() { m_testRepaint = true; }
    void repaintSweepHorizontally() { m_testRepaintSweepHorizontally = true; }
    void display();

    unsigned numberOfActiveAnimations() const;
    bool pauseAnimationAtTimeOnElementWithId(JSStringRef animationName, double time, JSStringRef elementId);

private:
    LayoutTestController(const std::string& testPathOrURL);

    bool m_dumpAsText;
    bool m_dumpStatusCallbacks;
    bool m_waitToDump; // True if waitUntilDone() has been called, but notifyDone() has not yet been called.
    bool m_testRepaint;
    bool m_testRepaintSweepHorizontally;

    std::string m_testPathOrURL;
    
    RetainPtr<CFRunLoopTimerRef> m_waitToDumpWatchdog;
};

} // namespace WTR

#endif // LayoutTestController_h