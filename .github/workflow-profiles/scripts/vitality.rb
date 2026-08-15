#!/usr/bin/env ruby
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# frozen_string_literal: true

# ==============================================================================
# 🩺 vitality.rb
# ------------------------------------------------------------------------------
# A standalone Ruby script that audits TODO comments across a repository.
#
# It enforces:
# - TODOs must include a date in the format: TODO(YYYY-MM-DD)
# - TODOs older than a configurable threshold are treated as errors
# - Undated TODOs are treated as warnings
#
# ------------------------------------------------------------------------------
# 🚀 USAGE
#
#   ruby vitality.rb [--threshold DAYS] [--path PATH]
#
# OPTIONS:
#   --threshold DAYS   Maximum allowed age of TODOs (default: 30)
#   --path PATH        Directory to scan (default: current directory)
#   --help             Show help message
#
# ------------------------------------------------------------------------------
# 🧪 EXIT CODES
#
#   0   Success (no expired TODOs)
#   1   Failure (expired TODOs found)
#   2   Invalid usage / argument error
#
# ------------------------------------------------------------------------------
# 🌱 ENVIRONMENT VARIABLES
#
#   DEBUG=1            Enable debug logging
#
# ==============================================================================

require 'date'
require 'optparse'

# ------------------------------------------------------------------------------
# Logging Helpers
# ------------------------------------------------------------------------------

def debug_log(message)
  return unless ENV['DEBUG'] == '1'

  warn "[DEBUG] #{message}"
end

def info_log(message)
  $stdout.puts message
end

def warn_log(message)
  warn message
end

def error_log(message)
  warn message
end

# ------------------------------------------------------------------------------
# Vitality Auditor
# ------------------------------------------------------------------------------

class VitalityAuditor
  DEFAULT_THRESHOLD_DAYS = 30

  def initialize(threshold_days:, root_path:)
    @threshold_days = threshold_days
    @root_path = root_path
    @errors = []
    @warnings = []
  end

  def run
    info_log '### 🔍 Scanning Ruby files for TODOs...'
    scan_files
    report_and_exit
  end

  private

  def scan_files
    pattern = File.join(@root_path, '**', '*.rb')

    Dir.glob(pattern).each do |file|
      next if skip_file?(file)

      debug_log "Scanning file: #{file}"

      File.foreach(file).with_index(1) do |line, line_number|
        check_line(line, file, line_number)
      end
    end
  end

  def skip_file?(file)
    file.include?('/vendor/') || file.include?('/.git/')
  end

  def check_line(line, file, line_number)
    # Match TODO(YYYY-MM-DD)
    dated_match = line.match(/TODO\((\d{4}-\d{2}-\d{2})\)/)

    if dated_match
      handle_dated_todo(dated_match[1], file, line_number)
    elsif line.include?('TODO')
      handle_undated_todo(file, line_number)
    end
  end

  def handle_dated_todo(date_string, file, line_number)
    date_added = parse_date_safe(date_string)
    return unless date_added

    @errors << format_error(file, line_number, date_added) if expired?(date_added)
  end

  def handle_undated_todo(file, line_number)
    @warnings << "⚠️  Undated TODO found in #{file}:#{line_number}"
  end

  def parse_date_safe(date_string)
    Date.parse(date_string)
  rescue ArgumentError
    warn_log "⚠️  Invalid date format in TODO: #{date_string}"
    nil
  end

  def expired?(date)
    date < (Date.today - @threshold_days)
  end

  def format_error(file, line_number, date)
    "⏰ Expired TODO in #{file}:#{line_number} (Added: #{date})"
  end

  def report_and_exit
    info_log "\n## 📊 Audit Results"

    @warnings.each do |warning|
      warn_log warning
    end

    if @errors.any?
      error_log "\n### ❌ Vitality Check Failed"
      @errors.each do |error|
        error_log "  - #{error}"
      end
      exit 1
    end

    info_log "\n### ✅ Project is Fresh!"
    info_log "All TODOs are within the #{@threshold_days}-day limit."
    exit 0
  end
end

# ------------------------------------------------------------------------------
# CLI Parsing
# ------------------------------------------------------------------------------

options = {
  threshold_days: VitalityAuditor::DEFAULT_THRESHOLD_DAYS,
  root_path: '.',
}

parser = OptionParser.new do |opts|
  opts.banner = 'Usage: vitality.rb [options]'

  opts.on('--threshold DAYS', Integer, 'Max age of TODOs (default: 30)') do |value|
    options[:threshold_days] = value
  end

  opts.on('--path PATH', String, 'Path to scan (default: .)') do |value|
    options[:root_path] = value
  end

  opts.on('--help', 'Show this help message') do
    $stdout.puts opts
    exit 0
  end
end

begin
  parser.parse!
rescue OptionParser::InvalidOption, OptionParser::MissingArgument => e
  error_log e.message
  error_log parser
  exit 2
end

# ------------------------------------------------------------------------------
# Execution
# ------------------------------------------------------------------------------

auditor = VitalityAuditor.new(
  threshold_days: options[:threshold_days],
  root_path: options[:root_path],
)

auditor.run
