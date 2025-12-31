### MediaBrowser.MediaEncoding

# Project Directory Structure
```
./
│   MediaBrowser.MediaEncoding.csproj
├── Probing/
├── │   MediaFrameSideDataInfo.cs
├── │   MediaFrameInfo.cs
├── │   FFProbeHelpers.cs
├── │   CodecType.cs
├── │   MediaStreamInfo.cs
├── │   ProbeResultNormalizer.cs
├── │   MediaFormatInfo.cs
├── │   MediaChapter.cs
├── │   InternalMediaInfoResult.cs
├── │   MediaStreamInfoSideData.cs
├── Encoder/
├── │   EncoderValidator.cs
├── │   MediaEncoder.cs
├── │   ApplePlatformHelper.cs
├── │   EncodingUtils.cs
├── Configuration/
├── │   EncodingConfigurationStore.cs
├── │   EncodingConfigurationFactory.cs
├── Attachments/
├── │   AttachmentExtractor.cs
├── Subtitles/
├── │   ISubtitleParser.cs
├── │   SsaWriter.cs
├── │   VttWriter.cs
├── │   JsonWriter.cs
├── │   SubtitleFormatExtensions.cs
├── │   TtmlWriter.cs
├── │   SubtitleEncoder.cs
├── │   ISubtitleWriter.cs
├── │   SrtWriter.cs
├── │   AssWriter.cs
├── │   SubtitleEditParser.cs
├── BdInfo/
├── │   BdInfoExaminer.cs
├── │   BdInfoFileInfo.cs
├── │   BdInfoDirectoryInfo.cs
├── Transcoding/
├── │   TranscodeManager.cs
├── Properties/
├── │   AssemblyInfo.cs```

# Probing/MediaFrameSideDataInfo.cs
using System.Text.Json.Serialization;

namespace MediaBrowser.MediaEncoding.Probing;

/// <summary>
/// Class MediaFrameSideDataInfo.
/// Currently only records the SideDataType for HDR10+ detection.
/// </summary>
public class MediaFrameSideDataInfo
{
    /// <summary>
    /// Gets or sets the SideDataType.
    /// </summary>
    [JsonPropertyName("side_data_type")]
    public string? SideDataType { get; set; }
}


# Probing/MediaFrameInfo.cs
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace MediaBrowser.MediaEncoding.Probing;

/// <summary>
/// Class MediaFrameInfo.
/// </summary>
public class MediaFrameInfo
{
    /// <summary>
    /// Gets or sets the media type.
    /// </summary>
    [JsonPropertyName("media_type")]
    public string? MediaType { get; set; }

    /// <summary>
    /// Gets or sets the StreamIndex.
    /// </summary>
    [JsonPropertyName("stream_index")]
    public int? StreamIndex { get; set; }

    /// <summary>
    /// Gets or sets the KeyFrame.
    /// </summary>
    [JsonPropertyName("key_frame")]
    public int? KeyFrame { get; set; }

    /// <summary>
    /// Gets or sets the Pts.
    /// </summary>
    [JsonPropertyName("pts")]
    public long? Pts { get; set; }

    /// <summary>
    /// Gets or sets the PtsTime.
    /// </summary>
    [JsonPropertyName("pts_time")]
    public string? PtsTime { get; set; }

    /// <summary>
    /// Gets or sets the BestEffortTimestamp.
    /// </summary>
    [JsonPropertyName("best_effort_timestamp")]
    public long BestEffortTimestamp { get; set; }

    /// <summary>
    /// Gets or sets the BestEffortTimestampTime.
    /// </summary>
    [JsonPropertyName("best_effort_timestamp_time")]
    public string? BestEffortTimestampTime { get; set; }

    /// <summary>
    /// Gets or sets the Duration.
    /// </summary>
    [JsonPropertyName("duration")]
    public int Duration { get; set; }

    /// <summary>
    /// Gets or sets the DurationTime.
    /// </summary>
    [JsonPropertyName("duration_time")]
    public string? DurationTime { get; set; }

    /// <summary>
    /// Gets or sets the PktPos.
    /// </summary>
    [JsonPropertyName("pkt_pos")]
    public string? PktPos { get; set; }

    /// <summary>
    /// Gets or sets the PktSize.
    /// </summary>
    [JsonPropertyName("pkt_size")]
    public string? PktSize { get; set; }

    /// <summary>
    /// Gets or sets the Width.
    /// </summary>
    [JsonPropertyName("width")]
    public int? Width { get; set; }

    /// <summary>
    /// Gets or sets the Height.
    /// </summary>
    [JsonPropertyName("height")]
    public int? Height { get; set; }

    /// <summary>
    /// Gets or sets the CropTop.
    /// </summary>
    [JsonPropertyName("crop_top")]
    public int? CropTop { get; set; }

    /// <summary>
    /// Gets or sets the CropBottom.
    /// </summary>
    [JsonPropertyName("crop_bottom")]
    public int? CropBottom { get; set; }

    /// <summary>
    /// Gets or sets the CropLeft.
    /// </summary>
    [JsonPropertyName("crop_left")]
    public int? CropLeft { get; set; }

    /// <summary>
    /// Gets or sets the CropRight.
    /// </summary>
    [JsonPropertyName("crop_right")]
    public int? CropRight { get; set; }

    /// <summary>
    /// Gets or sets the PixFmt.
    /// </summary>
    [JsonPropertyName("pix_fmt")]
    public string? PixFmt { get; set; }

    /// <summary>
    /// Gets or sets the SampleAspectRatio.
    /// </summary>
    [JsonPropertyName("sample_aspect_ratio")]
    public string? SampleAspectRatio { get; set; }

    /// <summary>
    /// Gets or sets the PictType.
    /// </summary>
    [JsonPropertyName("pict_type")]
    public string? PictType { get; set; }

    /// <summary>
    /// Gets or sets the InterlacedFrame.
    /// </summary>
    [JsonPropertyName("interlaced_frame")]
    public int? InterlacedFrame { get; set; }

    /// <summary>
    /// Gets or sets the TopFieldFirst.
    /// </summary>
    [JsonPropertyName("top_field_first")]
    public int? TopFieldFirst { get; set; }

    /// <summary>
    /// Gets or sets the RepeatPict.
    /// </summary>
    [JsonPropertyName("repeat_pict")]
    public int? RepeatPict { get; set; }

    /// <summary>
    /// Gets or sets the ColorRange.
    /// </summary>
    [JsonPropertyName("color_range")]
    public string? ColorRange { get; set; }

    /// <summary>
    /// Gets or sets the ColorSpace.
    /// </summary>
    [JsonPropertyName("color_space")]
    public string? ColorSpace { get; set; }

    /// <summary>
    /// Gets or sets the ColorPrimaries.
    /// </summary>
    [JsonPropertyName("color_primaries")]
    public string? ColorPrimaries { get; set; }

    /// <summary>
    /// Gets or sets the ColorTransfer.
    /// </summary>
    [JsonPropertyName("color_transfer")]
    public string? ColorTransfer { get; set; }

    /// <summary>
    /// Gets or sets the ChromaLocation.
    /// </summary>
    [JsonPropertyName("chroma_location")]
    public string? ChromaLocation { get; set; }

    /// <summary>
    /// Gets or sets the SideDataList.
    /// </summary>
    [JsonPropertyName("side_data_list")]
    public IReadOnlyList<MediaFrameSideDataInfo>? SideDataList { get; set; }
}


# Probing/FFProbeHelpers.cs
using System;
using System.Collections.Generic;
using System.Globalization;

namespace MediaBrowser.MediaEncoding.Probing
{
    /// <summary>
    /// Class containing helper methods for working with FFprobe output.
    /// </summary>
    public static class FFProbeHelpers
    {
        /// <summary>
        /// Normalizes the FF probe result.
        /// </summary>
        /// <param name="result">The result.</param>
        public static void NormalizeFFProbeResult(InternalMediaInfoResult result)
        {
            ArgumentNullException.ThrowIfNull(result);

            if (result.Format?.Tags is not null)
            {
                result.Format.Tags = ConvertDictionaryToCaseInsensitive(result.Format.Tags);
            }

            if (result.Streams is not null)
            {
                // Convert all dictionaries to case-insensitive
                foreach (var stream in result.Streams)
                {
                    if (stream.Tags is not null)
                    {
                        stream.Tags = ConvertDictionaryToCaseInsensitive(stream.Tags);
                    }
                }
            }
        }

        /// <summary>
        /// Gets an int from an FFProbeResult tags dictionary.
        /// </summary>
        /// <param name="tags">The tags.</param>
        /// <param name="key">The key.</param>
        /// <returns>System.Nullable{System.Int32}.</returns>
        public static int? GetDictionaryNumericValue(IReadOnlyDictionary<string, string> tags, string key)
        {
            if (tags.TryGetValue(key, out var val) && int.TryParse(val, out var i))
            {
                return i;
            }

            return null;
        }

        /// <summary>
        /// Gets a DateTime from an FFProbeResult tags dictionary.
        /// </summary>
        /// <param name="tags">The tags.</param>
        /// <param name="key">The key.</param>
        /// <returns>System.Nullable{DateTime}.</returns>
        public static DateTime? GetDictionaryDateTime(IReadOnlyDictionary<string, string> tags, string key)
        {
            if (tags.TryGetValue(key, out var val)
                && (DateTime.TryParse(val, DateTimeFormatInfo.CurrentInfo, DateTimeStyles.AssumeUniversal | DateTimeStyles.AdjustToUniversal, out var dateTime)
                    || DateTime.TryParseExact(val, "yyyy", DateTimeFormatInfo.CurrentInfo, DateTimeStyles.AssumeUniversal | DateTimeStyles.AdjustToUniversal, out dateTime)))
            {
                return dateTime;
            }

            return null;
        }

        /// <summary>
        /// Converts a dictionary to case-insensitive.
        /// </summary>
        /// <param name="dict">The dict.</param>
        /// <returns>Dictionary{System.StringSystem.String}.</returns>
        private static Dictionary<string, string> ConvertDictionaryToCaseInsensitive(IReadOnlyDictionary<string, string> dict)
        {
            return new Dictionary<string, string>(dict, StringComparer.OrdinalIgnoreCase);
        }
    }
}


# Probing/CodecType.cs
namespace MediaBrowser.MediaEncoding.Probing;

/// <summary>
/// FFmpeg Codec Type.
/// </summary>
public enum CodecType
{
    /// <summary>
    /// Video.
    /// </summary>
    Video,

    /// <summary>
    /// Audio.
    /// </summary>
    Audio,

    /// <summary>
    /// Opaque data information usually continuous.
    /// </summary>
    Data,

    /// <summary>
    /// Subtitles.
    /// </summary>
    Subtitle,

    /// <summary>
    /// Opaque data information usually sparse.
    /// </summary>
    Attachment
}


# Probing/MediaStreamInfo.cs
#nullable disable

using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace MediaBrowser.MediaEncoding.Probing
{
    /// <summary>
    /// Represents a stream within the output.
    /// </summary>
    public class MediaStreamInfo
    {
        /// <summary>
        /// Gets or sets the index.
        /// </summary>
        /// <value>The index.</value>
        [JsonPropertyName("index")]
        public int Index { get; set; }

        /// <summary>
        /// Gets or sets the profile.
        /// </summary>
        /// <value>The profile.</value>
        [JsonPropertyName("profile")]
        public string Profile { get; set; }

        /// <summary>
        /// Gets or sets the codec_name.
        /// </summary>
        /// <value>The codec_name.</value>
        [JsonPropertyName("codec_name")]
        public string CodecName { get; set; }

        /// <summary>
        /// Gets or sets the codec_long_name.
        /// </summary>
        /// <value>The codec_long_name.</value>
        [JsonPropertyName("codec_long_name")]
        public string CodecLongName { get; set; }

        /// <summary>
        /// Gets or sets the codec_type.
        /// </summary>
        /// <value>The codec_type.</value>
        [JsonPropertyName("codec_type")]
        public CodecType CodecType { get; set; }

        /// <summary>
        /// Gets or sets the sample_rate.
        /// </summary>
        /// <value>The sample_rate.</value>
        [JsonPropertyName("sample_rate")]
        public string SampleRate { get; set; }

        /// <summary>
        /// Gets or sets the channels.
        /// </summary>
        /// <value>The channels.</value>
        [JsonPropertyName("channels")]
        public int Channels { get; set; }

        /// <summary>
        /// Gets or sets the channel_layout.
        /// </summary>
        /// <value>The channel_layout.</value>
        [JsonPropertyName("channel_layout")]
        public string ChannelLayout { get; set; }

        /// <summary>
        /// Gets or sets the avg_frame_rate.
        /// </summary>
        /// <value>The avg_frame_rate.</value>
        [JsonPropertyName("avg_frame_rate")]
        public string AverageFrameRate { get; set; }

        /// <summary>
        /// Gets or sets the duration.
        /// </summary>
        /// <value>The duration.</value>
        [JsonPropertyName("duration")]
        public string Duration { get; set; }

        /// <summary>
        /// Gets or sets the bit_rate.
        /// </summary>
        /// <value>The bit_rate.</value>
        [JsonPropertyName("bit_rate")]
        public string BitRate { get; set; }

        /// <summary>
        /// Gets or sets the width.
        /// </summary>
        /// <value>The width.</value>
        [JsonPropertyName("width")]
        public int Width { get; set; }

        /// <summary>
        /// Gets or sets the refs.
        /// </summary>
        /// <value>The refs.</value>
        [JsonPropertyName("refs")]
        public int Refs { get; set; }

        /// <summary>
        /// Gets or sets the height.
        /// </summary>
        /// <value>The height.</value>
        [JsonPropertyName("height")]
        public int Height { get; set; }

        /// <summary>
        /// Gets or sets the display_aspect_ratio.
        /// </summary>
        /// <value>The display_aspect_ratio.</value>
        [JsonPropertyName("display_aspect_ratio")]
        public string DisplayAspectRatio { get; set; }

        /// <summary>
        /// Gets or sets the tags.
        /// </summary>
        /// <value>The tags.</value>
        [JsonPropertyName("tags")]
        public IReadOnlyDictionary<string, string> Tags { get; set; }

        /// <summary>
        /// Gets or sets the bits_per_sample.
        /// </summary>
        /// <value>The bits_per_sample.</value>
        [JsonPropertyName("bits_per_sample")]
        public int BitsPerSample { get; set; }

        /// <summary>
        /// Gets or sets the bits_per_raw_sample.
        /// </summary>
        /// <value>The bits_per_raw_sample.</value>
        [JsonPropertyName("bits_per_raw_sample")]
        public int BitsPerRawSample { get; set; }

        /// <summary>
        /// Gets or sets the r_frame_rate.
        /// </summary>
        /// <value>The r_frame_rate.</value>
        [JsonPropertyName("r_frame_rate")]
        public string RFrameRate { get; set; }

        /// <summary>
        /// Gets or sets the has_b_frames.
        /// </summary>
        /// <value>The has_b_frames.</value>
        [JsonPropertyName("has_b_frames")]
        public int HasBFrames { get; set; }

        /// <summary>
        /// Gets or sets the sample_aspect_ratio.
        /// </summary>
        /// <value>The sample_aspect_ratio.</value>
        [JsonPropertyName("sample_aspect_ratio")]
        public string SampleAspectRatio { get; set; }

        /// <summary>
        /// Gets or sets the pix_fmt.
        /// </summary>
        /// <value>The pix_fmt.</value>
        [JsonPropertyName("pix_fmt")]
        public string PixelFormat { get; set; }

        /// <summary>
        /// Gets or sets the level.
        /// </summary>
        /// <value>The level.</value>
        [JsonPropertyName("level")]
        public int Level { get; set; }

        /// <summary>
        /// Gets or sets the time_base.
        /// </summary>
        /// <value>The time_base.</value>
        [JsonPropertyName("time_base")]
        public string TimeBase { get; set; }

        /// <summary>
        /// Gets or sets the start_time.
        /// </summary>
        /// <value>The start_time.</value>
        [JsonPropertyName("start_time")]
        public string StartTime { get; set; }

        /// <summary>
        /// Gets or sets the codec_time_base.
        /// </summary>
        /// <value>The codec_time_base.</value>
        [JsonPropertyName("codec_time_base")]
        public string CodecTimeBase { get; set; }

        /// <summary>
        /// Gets or sets the codec_tag.
        /// </summary>
        /// <value>The codec_tag.</value>
        [JsonPropertyName("codec_tag")]
        public string CodecTag { get; set; }

        /// <summary>
        /// Gets or sets the codec_tag_string.
        /// </summary>
        /// <value>The codec_tag_string.</value>
        [JsonPropertyName("codec_tag_string")]
        public string CodecTagString { get; set; }

        /// <summary>
        /// Gets or sets the sample_fmt.
        /// </summary>
        /// <value>The sample_fmt.</value>
        [JsonPropertyName("sample_fmt")]
        public string SampleFmt { get; set; }

        /// <summary>
        /// Gets or sets the dmix_mode.
        /// </summary>
        /// <value>The dmix_mode.</value>
        [JsonPropertyName("dmix_mode")]
        public string DmixMode { get; set; }

        /// <summary>
        /// Gets or sets the start_pts.
        /// </summary>
        /// <value>The start_pts.</value>
        [JsonPropertyName("start_pts")]
        public long StartPts { get; set; }

        /// <summary>
        /// Gets or sets a value indicating whether the stream is AVC.
        /// </summary>
        /// <value>The is_avc.</value>
        [JsonPropertyName("is_avc")]
        public bool IsAvc { get; set; }

        /// <summary>
        /// Gets or sets the nal_length_size.
        /// </summary>
        /// <value>The nal_length_size.</value>
        [JsonPropertyName("nal_length_size")]
        public string NalLengthSize { get; set; }

        /// <summary>
        /// Gets or sets the ltrt_cmixlev.
        /// </summary>
        /// <value>The ltrt_cmixlev.</value>
        [JsonPropertyName("ltrt_cmixlev")]
        public string LtrtCmixlev { get; set; }

        /// <summary>
        /// Gets or sets the ltrt_surmixlev.
        /// </summary>
        /// <value>The ltrt_surmixlev.</value>
        [JsonPropertyName("ltrt_surmixlev")]
        public string LtrtSurmixlev { get; set; }

        /// <summary>
        /// Gets or sets the loro_cmixlev.
        /// </summary>
        /// <value>The loro_cmixlev.</value>
        [JsonPropertyName("loro_cmixlev")]
        public string LoroCmixlev { get; set; }

        /// <summary>
        /// Gets or sets the loro_surmixlev.
        /// </summary>
        /// <value>The loro_surmixlev.</value>
        [JsonPropertyName("loro_surmixlev")]
        public string LoroSurmixlev { get; set; }

        /// <summary>
        /// Gets or sets the field_order.
        /// </summary>
        /// <value>The field_order.</value>
        [JsonPropertyName("field_order")]
        public string FieldOrder { get; set; }

        /// <summary>
        /// Gets or sets the disposition.
        /// </summary>
        /// <value>The disposition.</value>
        [JsonPropertyName("disposition")]
        public IReadOnlyDictionary<string, int> Disposition { get; set; }

        /// <summary>
        /// Gets or sets the color range.
        /// </summary>
        /// <value>The color range.</value>
        [JsonPropertyName("color_range")]
        public string ColorRange { get; set; }

        /// <summary>
        /// Gets or sets the color space.
        /// </summary>
        /// <value>The color space.</value>
        [JsonPropertyName("color_space")]
        public string ColorSpace { get; set; }

        /// <summary>
        /// Gets or sets the color transfer.
        /// </summary>
        /// <value>The color transfer.</value>
        [JsonPropertyName("color_transfer")]
        public string ColorTransfer { get; set; }

        /// <summary>
        /// Gets or sets the color primaries.
        /// </summary>
        /// <value>The color primaries.</value>
        [JsonPropertyName("color_primaries")]
        public string ColorPrimaries { get; set; }

        /// <summary>
        /// Gets or sets the side_data_list.
        /// </summary>
        /// <value>The side_data_list.</value>
        [JsonPropertyName("side_data_list")]
        public IReadOnlyList<MediaStreamInfoSideData> SideDataList { get; set; }
    }
}


# Probing/ProbeResultNormalizer.cs
#nullable disable

using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Xml;
using Jellyfin.Data.Enums;
using Jellyfin.Extensions;
using MediaBrowser.Controller.Extensions;
using MediaBrowser.Controller.Library;
using MediaBrowser.Model.Dto;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.Globalization;
using MediaBrowser.Model.MediaInfo;
using Microsoft.Extensions.Logging;

namespace MediaBrowser.MediaEncoding.Probing
{
    /// <summary>
    /// Class responsible for normalizing FFprobe output.
    /// </summary>
    public partial class ProbeResultNormalizer
    {
        // When extracting subtitles, the maximum length to consider (to avoid invalid filenames)
        private const int MaxSubtitleDescriptionExtractionLength = 100;

        private const string ArtistReplaceValue = " | ";

        private static readonly char[] _basicDelimiters = ['/', ';'];
        private static readonly char[] _nameDelimiters = [.. _basicDelimiters, '|', '\\'];
        private static readonly char[] _genreDelimiters = [.. _basicDelimiters, ','];
        private static readonly string[] _webmVideoCodecs = ["av1", "vp8", "vp9"];
        private static readonly string[] _webmAudioCodecs = ["opus", "vorbis"];

        private readonly ILogger _logger;
        private readonly ILocalizationManager _localization;

        private string[] _splitWhiteList;

        /// <summary>
        /// Initializes a new instance of the <see cref="ProbeResultNormalizer"/> class.
        /// </summary>
        /// <param name="logger">The <see cref="ILogger{ProbeResultNormalizer}"/> for use with the <see cref="ProbeResultNormalizer"/> instance.</param>
        /// <param name="localization">The <see cref="ILocalizationManager"/> for use with the <see cref="ProbeResultNormalizer"/> instance.</param>
        public ProbeResultNormalizer(ILogger logger, ILocalizationManager localization)
        {
            _logger = logger;
            _localization = localization;
        }

        private IReadOnlyList<string> SplitWhitelist => _splitWhiteList ??= new string[]
        {
            "AC/DC",
            "A/T/O/S",
            "As/Hi Soundworks",
            "Au/Ra",
            "Bremer/McCoy",
            "b/bqスタヂオ",
            "DOV/S",
            "DJ'TEKINA//SOMETHING",
            "IX/ON",
            "J-CORE SLi//CER",
            "M(a/u)SH",
            "Kaoru/Brilliance",
            "signum/ii",
            "Richiter(LORB/DUGEM DI BARAT)",
            "이달의 소녀 1/3",
            "R!N / Gemie",
            "LOONA 1/3",
            "LOONA / yyxy",
            "LOONA / ODD EYE CIRCLE",
            "K/DA",
            "22/7",
            "諭吉佳作/men",
            "//dARTH nULL",
            "Phantom/Ghost",
            "She/Her/Hers",
            "5/8erl in Ehr'n",
            "Smith/Kotzen",
            "We;Na",
            "LSR/CITY",
        };

        /// <summary>
        /// Transforms a FFprobe response into its <see cref="MediaInfo"/> equivalent.
        /// </summary>
        /// <param name="data">The <see cref="InternalMediaInfoResult"/>.</param>
        /// <param name="videoType">The <see cref="VideoType"/>.</param>
        /// <param name="isAudio">A boolean indicating whether the media is audio.</param>
        /// <param name="path">Path to media file.</param>
        /// <param name="protocol">Path media protocol.</param>
        /// <returns>The <see cref="MediaInfo"/>.</returns>
        public MediaInfo GetMediaInfo(InternalMediaInfoResult data, VideoType? videoType, bool isAudio, string path, MediaProtocol protocol)
        {
            var info = new MediaInfo
            {
                Path = path,
                Protocol = protocol,
                VideoType = videoType
            };

            FFProbeHelpers.NormalizeFFProbeResult(data);
            SetSize(data, info);

            var internalStreams = data.Streams ?? Array.Empty<MediaStreamInfo>();
            var internalFrames = data.Frames ?? Array.Empty<MediaFrameInfo>();

            info.MediaStreams = internalStreams.Select(s => GetMediaStream(isAudio, s, data.Format, internalFrames))
                .Where(i => i is not null)
                // Drop subtitle streams if we don't know the codec because it will just cause failures if we don't know how to handle them
                .Where(i => i.Type != MediaStreamType.Subtitle || !string.IsNullOrWhiteSpace(i.Codec))
                .ToList();

            info.MediaAttachments = internalStreams.Select(GetMediaAttachment)
                .Where(i => i is not null)
                .ToList();

            if (data.Format is not null)
            {
                info.Container = NormalizeFormat(data.Format.FormatName, info.MediaStreams);

                if (int.TryParse(data.Format.BitRate, CultureInfo.InvariantCulture, out var value))
                {
                    info.Bitrate = value;
                }
            }

            var tags = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
            var tagStreamType = isAudio ? CodecType.Audio : CodecType.Video;

            var tagStream = data.Streams?.FirstOrDefault(i => i.CodecType == tagStreamType);

            if (tagStream?.Tags is not null)
            {
                foreach (var (key, value) in tagStream.Tags)
                {
                    tags[key] = value;
                }
            }

            if (data.Format?.Tags is not null)
            {
                foreach (var (key, value) in data.Format.Tags)
                {
                    tags[key] = value;
                }
            }

            FetchGenres(info, tags);

            info.Name = tags.GetFirstNotNullNorWhiteSpaceValue("title", "title-eng");
            info.ForcedSortName = tags.GetFirstNotNullNorWhiteSpaceValue("sort_name", "title-sort", "titlesort");
            info.Overview = tags.GetFirstNotNullNorWhiteSpaceValue("synopsis", "description", "desc", "comment");

            info.ParentIndexNumber = FFProbeHelpers.GetDictionaryNumericValue(tags, "season_number");
            info.IndexNumber = FFProbeHelpers.GetDictionaryNumericValue(tags, "episode_sort") ??
                               FFProbeHelpers.GetDictionaryNumericValue(tags, "episode_id");
            info.ShowName = tags.GetValueOrDefault("show_name", "show");
            info.ProductionYear = FFProbeHelpers.GetDictionaryNumericValue(tags, "date");

            // Several different forms of retail/premiere date
            info.PremiereDate =
                FFProbeHelpers.GetDictionaryDateTime(tags, "originaldate") ??
                FFProbeHelpers.GetDictionaryDateTime(tags, "retaildate") ??
                FFProbeHelpers.GetDictionaryDateTime(tags, "retail date") ??
                FFProbeHelpers.GetDictionaryDateTime(tags, "retail_date") ??
                FFProbeHelpers.GetDictionaryDateTime(tags, "date_released") ??
                FFProbeHelpers.GetDictionaryDateTime(tags, "date") ??
                FFProbeHelpers.GetDictionaryDateTime(tags, "creation_time");

            // Set common metadata for music (audio) and music videos (video)
            info.Album = tags.GetValueOrDefault("album");

            if (tags.TryGetValue("artists", out var artists) && !string.IsNullOrWhiteSpace(artists))
            {
                info.Artists = SplitDistinctArtists(artists, _basicDelimiters, false).ToArray();
            }
            else
            {
                var artist = tags.GetFirstNotNullNorWhiteSpaceValue("artist");
                info.Artists = artist is null
                    ? Array.Empty<string>()
                    : SplitDistinctArtists(artist, _nameDelimiters, true).ToArray();
            }

            // Guess ProductionYear from PremiereDate if missing
            if (!info.ProductionYear.HasValue && info.PremiereDate.HasValue)
            {
                info.ProductionYear = info.PremiereDate.Value.Year;
            }

            // Set mediaType-specific metadata
            if (isAudio)
            {
                SetAudioRuntimeTicks(data, info);

                // tags are normally located under data.format, but we've seen some cases with ogg where they're part of the info stream
                // so let's create a combined list of both

                SetAudioInfoFromTags(info, tags);
            }
            else
            {
                FetchStudios(info, tags, "copyright");

                var iTunExtc = tags.GetFirstNotNullNorWhiteSpaceValue("iTunEXTC");
                if (iTunExtc is not null)
                {
                    var parts = iTunExtc.Split('|', StringSplitOptions.RemoveEmptyEntries);
                    // Example
                    // mpaa|G|100|For crude humor
                    if (parts.Length > 1)
                    {
                        info.OfficialRating = parts[1];

                        if (parts.Length > 3)
                        {
                            info.OfficialRatingDescription = parts[3];
                        }
                    }
                }

                var iTunXml = tags.GetFirstNotNullNorWhiteSpaceValue("iTunMOVI");
                if (iTunXml is not null)
                {
                    FetchFromItunesInfo(iTunXml, info);
                }

                if (data.Format is not null && !string.IsNullOrEmpty(data.Format.Duration))
                {
                    info.RunTimeTicks = TimeSpan.FromSeconds(double.Parse(data.Format.Duration, CultureInfo.InvariantCulture)).Ticks;
                }

                FetchWtvInfo(info, data);

                if (data.Chapters is not null)
                {
                    info.Chapters = data.Chapters.Select(GetChapterInfo).ToArray();
                }

                ExtractTimestamp(info);

                if (tags.TryGetValue("stereo_mode", out var stereoMode) && string.Equals(stereoMode, "left_right", StringComparison.OrdinalIgnoreCase))
                {
                    info.Video3DFormat = Video3DFormat.FullSideBySide;
                }

                foreach (var mediaStream in info.MediaStreams)
                {
                    if (mediaStream.Type == MediaStreamType.Audio && !mediaStream.BitRate.HasValue)
                    {
                        mediaStream.BitRate = GetEstimatedAudioBitrate(mediaStream.Codec, mediaStream.Channels);
                    }
                }

                var videoStreamsBitrate = info.MediaStreams.Where(i => i.Type == MediaStreamType.Video).Select(i => i.BitRate ?? 0).Sum();
                // If ffprobe reported the container bitrate as being the same as the video stream bitrate, then it's wrong
                if (videoStreamsBitrate == (info.Bitrate ?? 0))
                {
                    info.InferTotalBitrate(true);
                }
            }

            return info;
        }

        private string NormalizeFormat(string format, IReadOnlyList<MediaStream> mediaStreams)
        {
            if (string.IsNullOrWhiteSpace(format))
            {
                return null;
            }

            // Input can be a list of multiple, comma-delimited formats - each of them needs to be checked
            var splitFormat = format.Split(',');
            for (var i = 0; i < splitFormat.Length; i++)
            {
                // Handle MPEG-1 container
                if (string.Equals(splitFormat[i], "mpegvideo", StringComparison.OrdinalIgnoreCase))
                {
                    splitFormat[i] = "mpeg";
                }

                // Handle MPEG-TS container
                else if (string.Equals(splitFormat[i], "mpegts", StringComparison.OrdinalIgnoreCase))
                {
                    splitFormat[i] = "ts";
                }

                // Handle matroska container
                else if (string.Equals(splitFormat[i], "matroska", StringComparison.OrdinalIgnoreCase))
                {
                    splitFormat[i] = "mkv";
                }

                // Handle WebM
                else if (string.Equals(splitFormat[i], "webm", StringComparison.OrdinalIgnoreCase))
                {
                    // Limit WebM to supported codecs
                    if (mediaStreams.Any(stream => (stream.Type == MediaStreamType.Video && !_webmVideoCodecs.Contains(stream.Codec, StringComparison.OrdinalIgnoreCase))
                        || (stream.Type == MediaStreamType.Audio && !_webmAudioCodecs.Contains(stream.Codec, StringComparison.OrdinalIgnoreCase))))
                    {
                        splitFormat[i] = string.Empty;
                    }
                }
            }

            return string.Join(',', splitFormat.Where(s => !string.IsNullOrEmpty(s)));
        }

        private static int? GetEstimatedAudioBitrate(string codec, int? channels)
        {
            if (!channels.HasValue)
            {
                return null;
            }

            var channelsValue = channels.Value;

            if (string.Equals(codec, "aac", StringComparison.OrdinalIgnoreCase)
                || string.Equals(codec, "mp3", StringComparison.OrdinalIgnoreCase))
            {
                switch (channelsValue)
                {
                    case <= 2:
                        return 192000;
                    case >= 5:
                        return 320000;
                }
            }

            if (string.Equals(codec, "ac3", StringComparison.OrdinalIgnoreCase)
                || string.Equals(codec, "eac3", StringComparison.OrdinalIgnoreCase))
            {
                switch (channelsValue)
                {
                    case <= 2:
                        return 192000;
                    case >= 5:
                        return 640000;
                }
            }

            if (string.Equals(codec, "flac", StringComparison.OrdinalIgnoreCase)
                || string.Equals(codec, "alac", StringComparison.OrdinalIgnoreCase))
            {
                switch (channelsValue)
                {
                    case <= 2:
                        return 960000;
                    case >= 5:
                        return 2880000;
                }
            }

            return null;
        }

        private void FetchFromItunesInfo(string xml, MediaInfo info)
        {
            // Make things simpler and strip out the dtd
            var plistIndex = xml.IndexOf("<plist", StringComparison.OrdinalIgnoreCase);

            if (plistIndex != -1)
            {
                xml = xml.Substring(plistIndex);
            }

            xml = "<?xml version=\"1.0\"?>" + xml;

            // <?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n<plist version=\"1.0\">\n<dict>\n\t<key>cast</key>\n\t<array>\n\t\t<dict>\n\t\t\t<key>name</key>\n\t\t\t<string>Blender Foundation</string>\n\t\t</dict>\n\t\t<dict>\n\t\t\t<key>name</key>\n\t\t\t<string>Janus Bager Kristensen</string>\n\t\t</dict>\n\t</array>\n\t<key>directors</key>\n\t<array>\n\t\t<dict>\n\t\t\t<key>name</key>\n\t\t\t<string>Sacha Goedegebure</string>\n\t\t</dict>\n\t</array>\n\t<key>studio</key>\n\t<string>Blender Foundation</string>\n</dict>\n</plist>\n
            using (var stream = new MemoryStream(Encoding.UTF8.GetBytes(xml)))
            using (var streamReader = new StreamReader(stream))
            {
                try
                {
                    using (var reader = XmlReader.Create(streamReader))
                    {
                        reader.MoveToContent();
                        reader.Read();

                        // Loop through each element
                        while (!reader.EOF && reader.ReadState == ReadState.Interactive)
                        {
                            if (reader.NodeType == XmlNodeType.Element)
                            {
                                switch (reader.Name)
                                {
                                    case "dict":
                                        if (reader.IsEmptyElement)
                                        {
                                            reader.Read();
                                            continue;
                                        }

                                        using (var subtree = reader.ReadSubtree())
                                        {
                                            ReadFromDictNode(subtree, info);
                                        }

                                        break;
                                    default:
                                        reader.Skip();
                                        break;
                                }
                            }
                            else
                            {
                                reader.Read();
                            }
                        }
                    }
                }
                catch (XmlException)
                {
                    // I've seen probe examples where the iTunMOVI value is just "<"
                    // So we should not allow this to fail the entire probing operation
                }
            }
        }

        private void ReadFromDictNode(XmlReader reader, MediaInfo info)
        {
            string currentKey = null;
            var pairs = new List<NameValuePair>();

            reader.MoveToContent();
            reader.Read();

            // Loop through each element
            while (!reader.EOF && reader.ReadState == ReadState.Interactive)
            {
                if (reader.NodeType == XmlNodeType.Element)
                {
                    switch (reader.Name)
                    {
                        case "key":
                            if (!string.IsNullOrWhiteSpace(currentKey))
                            {
                                ProcessPairs(currentKey, pairs, info);
                            }

                            currentKey = reader.ReadElementContentAsString();
                            pairs = new List<NameValuePair>();
                            break;
                        case "string":
                            var value = reader.ReadElementContentAsString();
                            if (!string.IsNullOrWhiteSpace(value))
                            {
                                pairs.Add(new NameValuePair
                                {
                                    Name = value,
                                    Value = value
                                });
                            }

                            break;
                        case "array":
                            if (reader.IsEmptyElement)
                            {
                                reader.Read();
                                continue;
                            }

                            using (var subtree = reader.ReadSubtree())
                            {
                                if (!string.IsNullOrWhiteSpace(currentKey))
                                {
                                    pairs.AddRange(ReadValueArray(subtree));
                                }
                            }

                            break;
                        default:
                            reader.Skip();
                            break;
                    }
                }
                else
                {
                    reader.Read();
                }
            }
        }

        private List<NameValuePair> ReadValueArray(XmlReader reader)
        {
            var pairs = new List<NameValuePair>();

            reader.MoveToContent();
            reader.Read();

            // Loop through each element
            while (!reader.EOF && reader.ReadState == ReadState.Interactive)
            {
                if (reader.NodeType == XmlNodeType.Element)
                {
                    switch (reader.Name)
                    {
                        case "dict":

                            if (reader.IsEmptyElement)
                            {
                                reader.Read();
                                continue;
                            }

                            using (var subtree = reader.ReadSubtree())
                            {
                                var dict = GetNameValuePair(subtree);
                                if (dict is not null)
                                {
                                    pairs.Add(dict);
                                }
                            }

                            break;
                        default:
                            reader.Skip();
                            break;
                    }
                }
                else
                {
                    reader.Read();
                }
            }

            return pairs;
        }

        private static void ProcessPairs(string key, List<NameValuePair> pairs, MediaInfo info)
        {
            List<BaseItemPerson> peoples = new List<BaseItemPerson>();
            var distinctPairs = pairs.Select(p => p.Value)
                    .Where(i => !string.IsNullOrWhiteSpace(i))
                    .Trimmed()
                    .Distinct(StringComparer.OrdinalIgnoreCase);

            if (string.Equals(key, "studio", StringComparison.OrdinalIgnoreCase))
            {
                info.Studios = distinctPairs.ToArray();
            }
            else if (string.Equals(key, "screenwriters", StringComparison.OrdinalIgnoreCase))
            {
                foreach (var pair in distinctPairs)
                {
                    peoples.Add(new BaseItemPerson
                    {
                        Name = pair,
                        Type = PersonKind.Writer
                    });
                }
            }
            else if (string.Equals(key, "producers", StringComparison.OrdinalIgnoreCase))
            {
                foreach (var pair in distinctPairs)
                {
                    peoples.Add(new BaseItemPerson
                    {
                        Name = pair,
                        Type = PersonKind.Producer
                    });
                }
            }
            else if (string.Equals(key, "directors", StringComparison.OrdinalIgnoreCase))
            {
                foreach (var pair in distinctPairs)
                {
                    peoples.Add(new BaseItemPerson
                    {
                        Name = pair,
                        Type = PersonKind.Director
                    });
                }
            }

            info.People = peoples.ToArray();
        }

        private static NameValuePair GetNameValuePair(XmlReader reader)
        {
            string name = null;
            string value = null;

            reader.MoveToContent();
            reader.Read();

            // Loop through each element
            while (!reader.EOF && reader.ReadState == ReadState.Interactive)
            {
                if (reader.NodeType == XmlNodeType.Element)
                {
                    switch (reader.Name)
                    {
                        case "key":
                            name = reader.ReadNormalizedString();
                            break;
                        case "string":
                            value = reader.ReadNormalizedString();
                            break;
                        default:
                            reader.Skip();
                            break;
                    }
                }
                else
                {
                    reader.Read();
                }
            }

            if (string.IsNullOrEmpty(name)
                || string.IsNullOrEmpty(value))
            {
                return null;
            }

            return new NameValuePair
            {
                Name = name,
                Value = value
            };
        }

        private static string NormalizeSubtitleCodec(string codec)
        {
            if (string.Equals(codec, "dvb_subtitle", StringComparison.OrdinalIgnoreCase))
            {
                codec = "DVBSUB";
            }
            else if (string.Equals(codec, "dvb_teletext", StringComparison.OrdinalIgnoreCase))
            {
                codec = "DVBTXT";
            }
            else if (string.Equals(codec, "dvd_subtitle", StringComparison.OrdinalIgnoreCase))
            {
                codec = "DVDSUB"; // .sub+.idx
            }
            else if (string.Equals(codec, "hdmv_pgs_subtitle", StringComparison.OrdinalIgnoreCase))
            {
                codec = "PGSSUB"; // .sup
            }

            return codec;
        }

        /// <summary>
        /// Converts ffprobe stream info to our MediaAttachment class.
        /// </summary>
        /// <param name="streamInfo">The stream info.</param>
        /// <returns>MediaAttachments.</returns>
        private MediaAttachment GetMediaAttachment(MediaStreamInfo streamInfo)
        {
            if (streamInfo.CodecType != CodecType.Attachment
                && streamInfo.Disposition?.GetValueOrDefault("attached_pic") != 1)
            {
                return null;
            }

            var attachment = new MediaAttachment
            {
                Codec = streamInfo.CodecName,
                Index = streamInfo.Index
            };

            if (!string.IsNullOrWhiteSpace(streamInfo.CodecTagString))
            {
                attachment.CodecTag = streamInfo.CodecTagString;
            }

            if (streamInfo.Tags is not null)
            {
                attachment.FileName = GetDictionaryValue(streamInfo.Tags, "filename");
                attachment.MimeType = GetDictionaryValue(streamInfo.Tags, "mimetype");
                attachment.Comment = GetDictionaryValue(streamInfo.Tags, "comment");
            }

            return attachment;
        }

        /// <summary>
        /// Converts ffprobe stream info to our MediaStream class.
        /// </summary>
        /// <param name="isAudio">if set to <c>true</c> [is info].</param>
        /// <param name="streamInfo">The stream info.</param>
        /// <param name="formatInfo">The format info.</param>
        /// <param name="frameInfoList">The frame info.</param>
        /// <returns>MediaStream.</returns>
        private MediaStream GetMediaStream(bool isAudio, MediaStreamInfo streamInfo, MediaFormatInfo formatInfo, IReadOnlyList<MediaFrameInfo> frameInfoList)
        {
            // These are mp4 chapters
            if (string.Equals(streamInfo.CodecName, "mov_text", StringComparison.OrdinalIgnoreCase))
            {
                // Edit: but these are also sometimes subtitles?
                // return null;
            }

            var stream = new MediaStream
            {
                Codec = streamInfo.CodecName,
                Profile = streamInfo.Profile,
                Level = streamInfo.Level,
                Index = streamInfo.Index,
                PixelFormat = streamInfo.PixelFormat,
                NalLengthSize = streamInfo.NalLengthSize,
                TimeBase = streamInfo.TimeBase,
                CodecTimeBase = streamInfo.CodecTimeBase,
                IsAVC = streamInfo.IsAvc
            };

            // Filter out junk
            if (!string.IsNullOrWhiteSpace(streamInfo.CodecTagString) && !streamInfo.CodecTagString.Contains("[0]", StringComparison.OrdinalIgnoreCase))
            {
                stream.CodecTag = streamInfo.CodecTagString;
            }

            if (streamInfo.Tags is not null)
            {
                stream.Language = GetDictionaryValue(streamInfo.Tags, "language");
                stream.Comment = GetDictionaryValue(streamInfo.Tags, "comment");
                stream.Title = GetDictionaryValue(streamInfo.Tags, "title");
            }

            if (streamInfo.CodecType == CodecType.Audio)
            {
                stream.Type = MediaStreamType.Audio;
                stream.LocalizedDefault = _localization.GetLocalizedString("Default");
                stream.LocalizedExternal = _localization.GetLocalizedString("External");

                stream.Channels = streamInfo.Channels;

                if (int.TryParse(streamInfo.SampleRate, CultureInfo.InvariantCulture, out var sampleRate))
                {
                    stream.SampleRate = sampleRate;
                }

                stream.ChannelLayout = ParseChannelLayout(streamInfo.ChannelLayout);

                if (streamInfo.BitsPerSample > 0)
                {
                    stream.BitDepth = streamInfo.BitsPerSample;
                }
                else if (streamInfo.BitsPerRawSample > 0)
                {
                    stream.BitDepth = streamInfo.BitsPerRawSample;
                }

                if (string.IsNullOrEmpty(stream.Title))
                {
                    // mp4 missing track title workaround: fall back to handler_name if populated and not the default "SoundHandler"
                    string handlerName = GetDictionaryValue(streamInfo.Tags, "handler_name");
                    if (!string.IsNullOrEmpty(handlerName) && !string.Equals(handlerName, "SoundHandler", StringComparison.OrdinalIgnoreCase))
                    {
                        stream.Title = handlerName;
                    }
                }
            }
            else if (streamInfo.CodecType == CodecType.Subtitle)
            {
                stream.Type = MediaStreamType.Subtitle;
                stream.Codec = NormalizeSubtitleCodec(stream.Codec);
                stream.LocalizedUndefined = _localization.GetLocalizedString("Undefined");
                stream.LocalizedDefault = _localization.GetLocalizedString("Default");
                stream.LocalizedForced = _localization.GetLocalizedString("Forced");
                stream.LocalizedExternal = _localization.GetLocalizedString("External");
                stream.LocalizedHearingImpaired = _localization.GetLocalizedString("HearingImpaired");

                // Graphical subtitle may have width and height info
                stream.Width = streamInfo.Width;
                stream.Height = streamInfo.Height;

                if (string.IsNullOrEmpty(stream.Title))
                {
                    // mp4 missing track title workaround: fall back to handler_name if populated and not the default "SubtitleHandler"
                    string handlerName = GetDictionaryValue(streamInfo.Tags, "handler_name");
                    if (!string.IsNullOrEmpty(handlerName) && !string.Equals(handlerName, "SubtitleHandler", StringComparison.OrdinalIgnoreCase))
                    {
                        stream.Title = handlerName;
                    }
                }
            }
            else if (streamInfo.CodecType == CodecType.Video)
            {
                stream.AverageFrameRate = GetFrameRate(streamInfo.AverageFrameRate);
                stream.RealFrameRate = GetFrameRate(streamInfo.RFrameRate);

                stream.IsInterlaced = !string.IsNullOrWhiteSpace(streamInfo.FieldOrder)
                    && !string.Equals(streamInfo.FieldOrder, "progressive", StringComparison.OrdinalIgnoreCase);

                if (isAudio
                    || string.Equals(stream.Codec, "bmp", StringComparison.OrdinalIgnoreCase)
                    || string.Equals(stream.Codec, "gif", StringComparison.OrdinalIgnoreCase)
                    || string.Equals(stream.Codec, "png", StringComparison.OrdinalIgnoreCase)
                    || string.Equals(stream.Codec, "webp", StringComparison.OrdinalIgnoreCase))
                {
                    stream.Type = MediaStreamType.EmbeddedImage;
                }
                else if (string.Equals(stream.Codec, "mjpeg", StringComparison.OrdinalIgnoreCase))
                {
                    // How to differentiate between video and embedded image?
                    // The only difference I've seen thus far is presence of codec tag, also embedded images have high (unusual) framerates
                    if (!string.IsNullOrWhiteSpace(stream.CodecTag))
                    {
                        stream.Type = MediaStreamType.Video;
                    }
                    else
                    {
                        stream.Type = MediaStreamType.EmbeddedImage;
                    }
                }
                else
                {
                    stream.Type = MediaStreamType.Video;
                }

                stream.Width = streamInfo.Width;
                stream.Height = streamInfo.Height;
                stream.AspectRatio = GetAspectRatio(streamInfo);

                if (streamInfo.BitsPerSample > 0)
                {
                    stream.BitDepth = streamInfo.BitsPerSample;
                }
                else if (streamInfo.BitsPerRawSample > 0)
                {
                    stream.BitDepth = streamInfo.BitsPerRawSample;
                }

                if (!stream.BitDepth.HasValue)
                {
                    if (!string.IsNullOrEmpty(streamInfo.PixelFormat))
                    {
                        if (string.Equals(streamInfo.PixelFormat, "yuv420p", StringComparison.OrdinalIgnoreCase)
                            || string.Equals(streamInfo.PixelFormat, "yuv444p", StringComparison.OrdinalIgnoreCase))
                        {
                            stream.BitDepth = 8;
                        }
                        else if (string.Equals(streamInfo.PixelFormat, "yuv420p10le", StringComparison.OrdinalIgnoreCase)
                                 || string.Equals(streamInfo.PixelFormat, "yuv444p10le", StringComparison.OrdinalIgnoreCase))
                        {
                            stream.BitDepth = 10;
                        }
                        else if (string.Equals(streamInfo.PixelFormat, "yuv420p12le", StringComparison.OrdinalIgnoreCase)
                                 || string.Equals(streamInfo.PixelFormat, "yuv444p12le", StringComparison.OrdinalIgnoreCase))
                        {
                            stream.BitDepth = 12;
                        }
                    }
                }

                // http://stackoverflow.com/questions/17353387/how-to-detect-anamorphic-video-with-ffprobe
                if (string.Equals(streamInfo.SampleAspectRatio, "1:1", StringComparison.Ordinal))
                {
                    stream.IsAnamorphic = false;
                }
                else if (!string.Equals(streamInfo.SampleAspectRatio, "0:1", StringComparison.Ordinal))
                {
                    stream.IsAnamorphic = true;
                }
                else if (string.Equals(streamInfo.DisplayAspectRatio, "0:1", StringComparison.Ordinal))
                {
                    stream.IsAnamorphic = false;
                }
                else if (!string.Equals(
                             streamInfo.DisplayAspectRatio,
                             // Force GetAspectRatio() to derive ratio from Width/Height directly by using null DAR
                             GetAspectRatio(new MediaStreamInfo
                             {
                                 Width = streamInfo.Width,
                                 Height = streamInfo.Height,
                                 DisplayAspectRatio = null
                             }),
                             StringComparison.Ordinal))
                {
                    stream.IsAnamorphic = true;
                }
                else
                {
                    stream.IsAnamorphic = false;
                }

                if (streamInfo.Refs > 0)
                {
                    stream.RefFrames = streamInfo.Refs;
                }

                if (!string.IsNullOrEmpty(streamInfo.ColorRange))
                {
                    stream.ColorRange = streamInfo.ColorRange;
                }

                if (!string.IsNullOrEmpty(streamInfo.ColorSpace))
                {
                    stream.ColorSpace = streamInfo.ColorSpace;
                }

                if (!string.IsNullOrEmpty(streamInfo.ColorTransfer))
                {
                    stream.ColorTransfer = streamInfo.ColorTransfer;
                }

                if (!string.IsNullOrEmpty(streamInfo.ColorPrimaries))
                {
                    stream.ColorPrimaries = streamInfo.ColorPrimaries;
                }

                if (streamInfo.SideDataList is not null)
                {
                    foreach (var data in streamInfo.SideDataList)
                    {
                        // Parse Dolby Vision metadata from side_data
                        if (string.Equals(data.SideDataType, "DOVI configuration record", StringComparison.OrdinalIgnoreCase))
                        {
                            stream.DvVersionMajor = data.DvVersionMajor;
                            stream.DvVersionMinor = data.DvVersionMinor;
                            stream.DvProfile = data.DvProfile;
                            stream.DvLevel = data.DvLevel;
                            stream.RpuPresentFlag = data.RpuPresentFlag;
                            stream.ElPresentFlag = data.ElPresentFlag;
                            stream.BlPresentFlag = data.BlPresentFlag;
                            stream.DvBlSignalCompatibilityId = data.DvBlSignalCompatibilityId;
                        }

                        // Parse video rotation metadata from side_data
                        else if (string.Equals(data.SideDataType, "Display Matrix", StringComparison.OrdinalIgnoreCase))
                        {
                            stream.Rotation = data.Rotation;
                        }

                        // Parse video frame cropping metadata from side_data
                        // TODO: save them and make HW filters to apply them in HWA pipelines
                        else if (string.Equals(data.SideDataType, "Frame Cropping", StringComparison.OrdinalIgnoreCase))
                        {
                            // Streams containing artificially added frame cropping
                            // metadata should not be marked as anamorphic.
                            stream.IsAnamorphic = false;
                        }
                    }
                }

                var frameInfo = frameInfoList?.FirstOrDefault(i => i.StreamIndex == stream.Index);
                if (frameInfo?.SideDataList is not null
                    && frameInfo.SideDataList.Any(data => string.Equals(data.SideDataType, "HDR Dynamic Metadata SMPTE2094-40 (HDR10+)", StringComparison.OrdinalIgnoreCase)))
                {
                    stream.Hdr10PlusPresentFlag = true;
                }
            }
            else if (streamInfo.CodecType == CodecType.Data)
            {
                stream.Type = MediaStreamType.Data;
            }
            else
            {
                return null;
            }

            // Get stream bitrate
            var bitrate = 0;

            if (int.TryParse(streamInfo.BitRate, CultureInfo.InvariantCulture, out var value))
            {
                bitrate = value;
            }

            // The bitrate info of FLAC musics and some videos is included in formatInfo.
            if (bitrate == 0
                && formatInfo is not null
                && (stream.Type == MediaStreamType.Video || (isAudio && stream.Type == MediaStreamType.Audio)))
            {
                // If the stream info doesn't have a bitrate get the value from the media format info
                if (int.TryParse(formatInfo.BitRate, CultureInfo.InvariantCulture, out value))
                {
                    bitrate = value;
                }
            }

            if (bitrate > 0)
            {
                stream.BitRate = bitrate;
            }

            // Extract bitrate info from tag "BPS" if possible.
            if (!stream.BitRate.HasValue
                && (streamInfo.CodecType == CodecType.Audio
                    || streamInfo.CodecType == CodecType.Video))
            {
                var bps = GetBPSFromTags(streamInfo);
                if (bps > 0)
                {
                    stream.BitRate = bps;
                }
                else
                {
                    // Get average bitrate info from tag "NUMBER_OF_BYTES" and "DURATION" if possible.
                    var durationInSeconds = GetRuntimeSecondsFromTags(streamInfo);
                    var bytes = GetNumberOfBytesFromTags(streamInfo);
                    if (durationInSeconds is not null && durationInSeconds.Value >= 1 && bytes is not null)
                    {
                        bps = Convert.ToInt32(bytes * 8 / durationInSeconds, CultureInfo.InvariantCulture);
                        if (bps > 0)
                        {
                            stream.BitRate = bps;
                        }
                    }
                }
            }

            var disposition = streamInfo.Disposition;
            if (disposition is not null)
            {
                if (disposition.GetValueOrDefault("default") == 1)
                {
                    stream.IsDefault = true;
                }

                if (disposition.GetValueOrDefault("forced") == 1)
                {
                    stream.IsForced = true;
                }

                if (disposition.GetValueOrDefault("hearing_impaired") == 1)
                {
                    stream.IsHearingImpaired = true;
                }
            }

            NormalizeStreamTitle(stream);

            return stream;
        }

        private static void NormalizeStreamTitle(MediaStream stream)
        {
            if (string.Equals(stream.Title, "cc", StringComparison.OrdinalIgnoreCase)
                || stream.Type == MediaStreamType.EmbeddedImage)
            {
                stream.Title = null;
            }
        }

        /// <summary>
        /// Gets a string from an FFProbeResult tags dictionary.
        /// </summary>
        /// <param name="tags">The tags.</param>
        /// <param name="key">The key.</param>
        /// <returns>System.String.</returns>
        private static string GetDictionaryValue(IReadOnlyDictionary<string, string> tags, string key)
        {
            if (tags is null)
            {
                return null;
            }

            tags.TryGetValue(key, out var val);

            return val;
        }

        private static string ParseChannelLayout(string input)
        {
            if (string.IsNullOrEmpty(input))
            {
                return null;
            }

            return input.AsSpan().LeftPart('(').ToString();
        }

        private static string GetAspectRatio(MediaStreamInfo info)
        {
            var original = info.DisplayAspectRatio;

            var parts = (original ?? string.Empty).Split(':');
            if (!(parts.Length == 2
                    && int.TryParse(parts[0], CultureInfo.InvariantCulture, out var width)
                    && int.TryParse(parts[1], CultureInfo.InvariantCulture, out var height)
                    && width > 0
                    && height > 0))
            {
                width = info.Width;
                height = info.Height;
            }

            if (width > 0 && height > 0)
            {
                double ratio = width;
                ratio /= height;

                if (IsClose(ratio, 1.777777778, .03))
                {
                    return "16:9";
                }

                if (IsClose(ratio, 1.3333333333, .05))
                {
                    return "4:3";
                }

                if (IsClose(ratio, 1.41))
                {
                    return "1.41:1";
                }

                if (IsClose(ratio, 1.5))
                {
                    return "1.5:1";
                }

                if (IsClose(ratio, 1.6))
                {
                    return "1.6:1";
                }

                if (IsClose(ratio, 1.66666666667))
                {
                    return "5:3";
                }

                if (IsClose(ratio, 1.85, .02))
                {
                    return "1.85:1";
                }

                if (IsClose(ratio, 2.35, .025))
                {
                    return "2.35:1";
                }

                if (IsClose(ratio, 2.4, .025))
                {
                    return "2.40:1";
                }
            }

            return original;
        }

        private static bool IsClose(double d1, double d2, double variance = .005)
        {
            return Math.Abs(d1 - d2) <= variance;
        }

        /// <summary>
        /// Gets a frame rate from a string value in ffprobe output
        /// This could be a number or in the format of 2997/125.
        /// </summary>
        /// <param name="value">The value.</param>
        /// <returns>System.Nullable{System.Single}.</returns>
        internal static float? GetFrameRate(ReadOnlySpan<char> value)
        {
            if (value.IsEmpty)
            {
                return null;
            }

            int index = value.IndexOf('/');
            if (index == -1)
            {
                return null;
            }

            if (!float.TryParse(value[..index], NumberStyles.Integer, CultureInfo.InvariantCulture, out var dividend)
                || !float.TryParse(value[(index + 1)..], NumberStyles.Integer, CultureInfo.InvariantCulture, out var divisor))
            {
                return null;
            }

            return divisor == 0f ? null : dividend / divisor;
        }

        private static void SetAudioRuntimeTicks(InternalMediaInfoResult result, MediaInfo data)
        {
            // Get the first info stream
            var stream = result.Streams?.FirstOrDefault(s => s.CodecType == CodecType.Audio);
            if (stream is null)
            {
                return;
            }

            // Get duration from stream properties
            var duration = stream.Duration;

            // If it's not there go into format properties
            if (string.IsNullOrEmpty(duration))
            {
                duration = result.Format.Duration;
            }

            // If we got something, parse it
            if (!string.IsNullOrEmpty(duration))
            {
                data.RunTimeTicks = TimeSpan.FromSeconds(double.Parse(duration, CultureInfo.InvariantCulture)).Ticks;
            }
        }

        private static int? GetBPSFromTags(MediaStreamInfo streamInfo)
        {
            if (streamInfo?.Tags is null)
            {
                return null;
            }

            var bps = GetDictionaryValue(streamInfo.Tags, "BPS-eng") ?? GetDictionaryValue(streamInfo.Tags, "BPS");
            if (int.TryParse(bps, NumberStyles.Integer, CultureInfo.InvariantCulture, out var parsedBps))
            {
                return parsedBps;
            }

            return null;
        }

        private static double? GetRuntimeSecondsFromTags(MediaStreamInfo streamInfo)
        {
            if (streamInfo?.Tags is null)
            {
                return null;
            }

            var duration = GetDictionaryValue(streamInfo.Tags, "DURATION-eng") ?? GetDictionaryValue(streamInfo.Tags, "DURATION");
            if (TimeSpan.TryParse(duration, out var parsedDuration))
            {
                return parsedDuration.TotalSeconds;
            }

            return null;
        }

        private static long? GetNumberOfBytesFromTags(MediaStreamInfo streamInfo)
        {
            if (streamInfo?.Tags is null)
            {
                return null;
            }

            var numberOfBytes = GetDictionaryValue(streamInfo.Tags, "NUMBER_OF_BYTES-eng")
                                ?? GetDictionaryValue(streamInfo.Tags, "NUMBER_OF_BYTES");
            if (long.TryParse(numberOfBytes, NumberStyles.Integer, CultureInfo.InvariantCulture, out var parsedBytes))
            {
                return parsedBytes;
            }

            return null;
        }

        private static void SetSize(InternalMediaInfoResult data, MediaInfo info)
        {
            if (data.Format is null)
            {
                return;
            }

            info.Size = string.IsNullOrEmpty(data.Format.Size) ? null : long.Parse(data.Format.Size, CultureInfo.InvariantCulture);
        }

        private void SetAudioInfoFromTags(MediaInfo audio, Dictionary<string, string> tags)
        {
            var people = new List<BaseItemPerson>();
            if (tags.TryGetValue("composer", out var composer) && !string.IsNullOrWhiteSpace(composer))
            {
                foreach (var person in Split(composer, false))
                {
                    people.Add(new BaseItemPerson { Name = person, Type = PersonKind.Composer });
                }
            }

            if (tags.TryGetValue("conductor", out var conductor) && !string.IsNullOrWhiteSpace(conductor))
            {
                foreach (var person in Split(conductor, false))
                {
                    people.Add(new BaseItemPerson { Name = person, Type = PersonKind.Conductor });
                }
            }

            if (tags.TryGetValue("lyricist", out var lyricist) && !string.IsNullOrWhiteSpace(lyricist))
            {
                foreach (var person in Split(lyricist, false))
                {
                    people.Add(new BaseItemPerson { Name = person, Type = PersonKind.Lyricist });
                }
            }

            if (tags.TryGetValue("performer", out var performer) && !string.IsNullOrWhiteSpace(performer))
            {
                foreach (var person in Split(performer, false))
                {
                    Match match = PerformerRegex().Match(person);

                    // If the performer doesn't have any instrument/role associated, it won't match. In that case, chances are it's simply a band name, so we skip it.
                    if (match.Success)
                    {
                        people.Add(new BaseItemPerson
                        {
                            Name = match.Groups["name"].Value,
                            Type = PersonKind.Actor,
                            Role = CultureInfo.InvariantCulture.TextInfo.ToTitleCase(match.Groups["instrument"].Value)
                        });
                    }
                }
            }

            // In cases where there isn't sufficient information as to which role a writer performed on a recording, tagging software uses the "writer" tag.
            if (tags.TryGetValue("writer", out var writer) && !string.IsNullOrWhiteSpace(writer))
            {
                foreach (var person in Split(writer, false))
                {
                    people.Add(new BaseItemPerson { Name = person, Type = PersonKind.Writer });
                }
            }

            if (tags.TryGetValue("arranger", out var arranger) && !string.IsNullOrWhiteSpace(arranger))
            {
                foreach (var person in Split(arranger, false))
                {
                    people.Add(new BaseItemPerson { Name = person, Type = PersonKind.Arranger });
                }
            }

            if (tags.TryGetValue("engineer", out var engineer) && !string.IsNullOrWhiteSpace(engineer))
            {
                foreach (var person in Split(engineer, false))
                {
                    people.Add(new BaseItemPerson { Name = person, Type = PersonKind.Engineer });
                }
            }

            if (tags.TryGetValue("mixer", out var mixer) && !string.IsNullOrWhiteSpace(mixer))
            {
                foreach (var person in Split(mixer, false))
                {
                    people.Add(new BaseItemPerson { Name = person, Type = PersonKind.Mixer });
                }
            }

            if (tags.TryGetValue("remixer", out var remixer) && !string.IsNullOrWhiteSpace(remixer))
            {
                foreach (var person in Split(remixer, false))
                {
                    people.Add(new BaseItemPerson { Name = person, Type = PersonKind.Remixer });
                }
            }

            audio.People = people.ToArray();

            // Set album artist
            var albumArtist = tags.GetFirstNotNullNorWhiteSpaceValue("albumartist", "album artist", "album_artist");
            audio.AlbumArtists = albumArtist is not null
                ? SplitDistinctArtists(albumArtist, _nameDelimiters, true).ToArray()
                : Array.Empty<string>();

            // Set album artist to artist if empty
            if (audio.AlbumArtists.Length == 0)
            {
                audio.AlbumArtists = audio.Artists;
            }

            // Track number
            audio.IndexNumber = GetDictionaryTrackOrDiscNumber(tags, "track");

            // Disc number
            audio.ParentIndexNumber = GetDictionaryTrackOrDiscNumber(tags, "disc");

            // There's several values in tags may or may not be present
            FetchStudios(audio, tags, "organization");
            FetchStudios(audio, tags, "ensemble");
            FetchStudios(audio, tags, "publisher");
            FetchStudios(audio, tags, "label");

            // These support multiple values, but for now we only store the first.
            var mb = GetMultipleMusicBrainzId(tags.GetValueOrDefault("MusicBrainz Album Artist Id"))
                ?? GetMultipleMusicBrainzId(tags.GetValueOrDefault("MUSICBRAINZ_ALBUMARTISTID"));
            audio.TrySetProviderId(MetadataProvider.MusicBrainzAlbumArtist, mb);

            mb = GetMultipleMusicBrainzId(tags.GetValueOrDefault("MusicBrainz Artist Id"))
                ?? GetMultipleMusicBrainzId(tags.GetValueOrDefault("MUSICBRAINZ_ARTISTID"));
            audio.TrySetProviderId(MetadataProvider.MusicBrainzArtist, mb);

            mb = GetMultipleMusicBrainzId(tags.GetValueOrDefault("MusicBrainz Album Id"))
                ?? GetMultipleMusicBrainzId(tags.GetValueOrDefault("MUSICBRAINZ_ALBUMID"));
            audio.TrySetProviderId(MetadataProvider.MusicBrainzAlbum, mb);

            mb = GetMultipleMusicBrainzId(tags.GetValueOrDefault("MusicBrainz Release Group Id"))
                 ?? GetMultipleMusicBrainzId(tags.GetValueOrDefault("MUSICBRAINZ_RELEASEGROUPID"));
            audio.TrySetProviderId(MetadataProvider.MusicBrainzReleaseGroup, mb);

            mb = GetMultipleMusicBrainzId(tags.GetValueOrDefault("MusicBrainz Release Track Id"))
                 ?? GetMultipleMusicBrainzId(tags.GetValueOrDefault("MUSICBRAINZ_RELEASETRACKID"));
            audio.TrySetProviderId(MetadataProvider.MusicBrainzTrack, mb);
        }

        private static string GetMultipleMusicBrainzId(string value)
        {
            if (string.IsNullOrWhiteSpace(value))
            {
                return null;
            }

            return value.Split('/', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                .FirstOrDefault();
        }

        /// <summary>
        /// Splits the specified val.
        /// </summary>
        /// <param name="val">The val.</param>
        /// <param name="allowCommaDelimiter">if set to <c>true</c> [allow comma delimiter].</param>
        /// <returns>System.String[][].</returns>
        private string[] Split(string val, bool allowCommaDelimiter)
        {
            // Only use the comma as a delimiter if there are no slashes or pipes.
            // We want to be careful not to split names that have commas in them
            return !allowCommaDelimiter || _nameDelimiters.Any(i => val.Contains(i, StringComparison.Ordinal)) ?
                val.Split(_nameDelimiters, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries) :
                val.Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        }

        private IEnumerable<string> SplitDistinctArtists(string val, char[] delimiters, bool splitFeaturing)
        {
            if (splitFeaturing)
            {
                val = val.Replace(" featuring ", ArtistReplaceValue, StringComparison.OrdinalIgnoreCase)
                    .Replace(" feat. ", ArtistReplaceValue, StringComparison.OrdinalIgnoreCase);
            }

            var artistsFound = new List<string>();

            foreach (var whitelistArtist in SplitWhitelist)
            {
                var originalVal = val;
                val = val.Replace(whitelistArtist, "|", StringComparison.OrdinalIgnoreCase);

                if (!string.Equals(originalVal, val, StringComparison.OrdinalIgnoreCase))
                {
                    artistsFound.Add(whitelistArtist);
                }
            }

            var artists = val.Split(delimiters, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);

            artistsFound.AddRange(artists);
            return artistsFound.DistinctNames();
        }

        /// <summary>
        /// Gets the studios from the tags collection.
        /// </summary>
        /// <param name="info">The info.</param>
        /// <param name="tags">The tags.</param>
        /// <param name="tagName">Name of the tag.</param>
        private void FetchStudios(MediaInfo info, IReadOnlyDictionary<string, string> tags, string tagName)
        {
            var val = tags.GetValueOrDefault(tagName);

            if (string.IsNullOrEmpty(val))
            {
                return;
            }

            var studios = Split(val, true);
            var studioList = new List<string>();

            foreach (var studio in studios)
            {
                if (string.IsNullOrWhiteSpace(studio))
                {
                    continue;
                }

                // Don't add artist/album artist name to studios, even if it's listed there
                if (info.Artists.Contains(studio, StringComparison.OrdinalIgnoreCase)
                    || info.AlbumArtists.Contains(studio, StringComparison.OrdinalIgnoreCase))
                {
                    continue;
                }

                studioList.Add(studio);
            }

            info.Studios = studioList
                .Distinct(StringComparer.OrdinalIgnoreCase)
                .ToArray();
        }

        /// <summary>
        /// Gets the genres from the tags collection.
        /// </summary>
        /// <param name="info">The information.</param>
        /// <param name="tags">The tags.</param>
        private void FetchGenres(MediaInfo info, IReadOnlyDictionary<string, string> tags)
        {
            var genreVal = tags.GetValueOrDefault("genre");
            if (string.IsNullOrEmpty(genreVal))
            {
                return;
            }

            var genres = new List<string>(info.Genres);
            foreach (var genre in Split(genreVal, true))
            {
                if (string.IsNullOrEmpty(genre))
                {
                    continue;
                }

                genres.Add(genre);
            }

            info.Genres = genres
                .Distinct(StringComparer.OrdinalIgnoreCase)
                .ToArray();
        }

        /// <summary>
        /// Gets the track or disc number, which can be in the form of '1', or '1/3'.
        /// </summary>
        /// <param name="tags">The tags.</param>
        /// <param name="tagName">Name of the tag.</param>
        /// <returns>The track or disc number, or null, if missing or not parseable.</returns>
        private static int? GetDictionaryTrackOrDiscNumber(IReadOnlyDictionary<string, string> tags, string tagName)
        {
            var disc = tags.GetValueOrDefault(tagName);

            if (int.TryParse(disc.AsSpan().LeftPart('/'), out var discNum))
            {
                return discNum;
            }

            return null;
        }

        private static ChapterInfo GetChapterInfo(MediaChapter chapter)
        {
            var info = new ChapterInfo();

            if (chapter.Tags is not null && chapter.Tags.TryGetValue("title", out string name))
            {
                info.Name = name;
            }

            // Limit accuracy to milliseconds to match xml saving
            var secondsString = chapter.StartTime;

            if (double.TryParse(secondsString, CultureInfo.InvariantCulture, out var seconds))
            {
                var ms = Math.Round(TimeSpan.FromSeconds(seconds).TotalMilliseconds);
                info.StartPositionTicks = TimeSpan.FromMilliseconds(ms).Ticks;
            }

            return info;
        }

        private void FetchWtvInfo(MediaInfo video, InternalMediaInfoResult data)
        {
            var tags = data.Format?.Tags;

            if (tags is null)
            {
                return;
            }

            if (tags.TryGetValue("WM/Genre", out var genres) && !string.IsNullOrWhiteSpace(genres))
            {
                var genreList = genres.Split(_genreDelimiters, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);

                // If this is empty then don't overwrite genres that might have been fetched earlier
                if (genreList.Length > 0)
                {
                    video.Genres = genreList;
                }
            }

            if (tags.TryGetValue("WM/ParentalRating", out var officialRating) && !string.IsNullOrWhiteSpace(officialRating))
            {
                video.OfficialRating = officialRating;
            }

            if (tags.TryGetValue("WM/MediaCredits", out var people) && !string.IsNullOrEmpty(people))
            {
                video.People = Array.ConvertAll(
                    people.Split(_basicDelimiters, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries),
                    i => new BaseItemPerson { Name = i, Type = PersonKind.Actor });
            }

            if (tags.TryGetValue("WM/OriginalReleaseTime", out var year) && int.TryParse(year, NumberStyles.Integer, CultureInfo.InvariantCulture, out var parsedYear))
            {
                video.ProductionYear = parsedYear;
            }

            // Credit to MCEBuddy: https://mcebuddy2x.codeplex.com/
            // DateTime is reported along with timezone info (typically Z i.e. UTC hence assume None)
            if (tags.TryGetValue("WM/MediaOriginalBroadcastDateTime", out var premiereDateString) && DateTime.TryParse(year, null, DateTimeStyles.AdjustToUniversal, out var parsedDate))
            {
                video.PremiereDate = parsedDate;
            }

            var description = tags.GetValueOrDefault("WM/SubTitleDescription");

            var subTitle = tags.GetValueOrDefault("WM/SubTitle");

            // For below code, credit to MCEBuddy: https://mcebuddy2x.codeplex.com/

            // Sometimes for TV Shows the Subtitle field is empty and the subtitle description contains the subtitle, extract if possible. See ticket https://mcebuddy2x.codeplex.com/workitem/1910
            // The format is -> EPISODE/TOTAL_EPISODES_IN_SEASON. SUBTITLE: DESCRIPTION
            // OR -> COMMENT. SUBTITLE: DESCRIPTION
            // e.g. -> 4/13. The Doctor's Wife: Science fiction drama. When he follows a Time Lord distress signal, the Doctor puts Amy, Rory and his beloved TARDIS in grave danger. Also in HD. [AD,S]
            // e.g. -> CBeebies Bedtime Hour. The Mystery: Animated adventures of two friends who live on an island in the middle of the big city. Some of Abney and Teal's favourite objects are missing. [S]
            if (string.IsNullOrWhiteSpace(subTitle)
                && !string.IsNullOrWhiteSpace(description)
                && description.AsSpan()[..Math.Min(description.Length, MaxSubtitleDescriptionExtractionLength)].Contains(':')) // Check within the Subtitle size limit, otherwise from description it can get too long creating an invalid filename
            {
                string[] descriptionParts = description.Split(':');
                if (descriptionParts.Length > 0)
                {
                    string subtitle = descriptionParts[0];
                    try
                    {
                        // Check if it contains a episode number and season number
                        if (subtitle.Contains('/', StringComparison.Ordinal))
                        {
                            string[] subtitleParts = subtitle.Split(' ');
                            string[] numbers = subtitleParts[0].Replace(".", string.Empty, StringComparison.Ordinal).Split('/');
                            video.IndexNumber = int.Parse(numbers[0], CultureInfo.InvariantCulture);
                            // int totalEpisodesInSeason = int.Parse(numbers[1], CultureInfo.InvariantCulture);

                            // Skip the numbers, concatenate the rest, trim and set as new description
                            description = string.Join(' ', subtitleParts, 1, subtitleParts.Length - 1).Trim();
                        }
                        else if (subtitle.Contains('.', StringComparison.Ordinal))
                        {
                            var subtitleParts = subtitle.Split('.');
                            description = string.Join('.', subtitleParts, 1, subtitleParts.Length - 1).Trim();
                        }
                        else
                        {
                            description = subtitle.Trim();
                        }
                    }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, "Error while parsing subtitle field");

                        // Fallback to default parsing
                        if (subtitle.Contains('.', StringComparison.Ordinal))
                        {
                            var subtitleParts = subtitle.Split('.');
                            description = string.Join('.', subtitleParts, 1, subtitleParts.Length - 1).Trim();
                        }
                        else
                        {
                            description = subtitle.Trim();
                        }
                    }
                }
            }

            if (!string.IsNullOrWhiteSpace(description))
            {
                video.Overview = description;
            }
        }

        private void ExtractTimestamp(MediaInfo video)
        {
            if (video.VideoType != VideoType.VideoFile)
            {
                return;
            }

            if (!string.Equals(video.Container, "mpeg2ts", StringComparison.OrdinalIgnoreCase)
                && !string.Equals(video.Container, "m2ts", StringComparison.OrdinalIgnoreCase)
                && !string.Equals(video.Container, "ts", StringComparison.OrdinalIgnoreCase))
            {
                return;
            }

            try
            {
                video.Timestamp = GetMpegTimestamp(video.Path);
                _logger.LogDebug("Video has {Timestamp} timestamp", video.Timestamp);
            }
            catch (Exception ex)
            {
                video.Timestamp = null;
                _logger.LogError(ex, "Error extracting timestamp info from {Path}", video.Path);
            }
        }

        // REVIEW: find out why the byte array needs to be 197 bytes long and comment the reason
        private static TransportStreamTimestamp GetMpegTimestamp(string path)
        {
            var packetBuffer = new byte[197];

            using (var fs = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read, 1))
            {
                fs.ReadExactly(packetBuffer);
            }

            if (packetBuffer[0] == 71)
            {
                return TransportStreamTimestamp.None;
            }

            if ((packetBuffer[4] != 71) || (packetBuffer[196] != 71))
            {
                return TransportStreamTimestamp.None;
            }

            if ((packetBuffer[0] == 0) && (packetBuffer[1] == 0) && (packetBuffer[2] == 0) && (packetBuffer[3] == 0))
            {
                return TransportStreamTimestamp.Zero;
            }

            return TransportStreamTimestamp.Valid;
        }

        [GeneratedRegex("(?<name>.*) \\((?<instrument>.*)\\)")]
        private static partial Regex PerformerRegex();
    }
}


# Probing/MediaFormatInfo.cs
#nullable disable

using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace MediaBrowser.MediaEncoding.Probing
{
    /// <summary>
    /// Class MediaFormat.
    /// </summary>
    public class MediaFormatInfo
    {
        /// <summary>
        /// Gets or sets the filename.
        /// </summary>
        /// <value>The filename.</value>
        [JsonPropertyName("filename")]
        public string FileName { get; set; }

        /// <summary>
        /// Gets or sets the nb_streams.
        /// </summary>
        /// <value>The nb_streams.</value>
        [JsonPropertyName("nb_streams")]
        public int NbStreams { get; set; }

        /// <summary>
        /// Gets or sets the format_name.
        /// </summary>
        /// <value>The format_name.</value>
        [JsonPropertyName("format_name")]
        public string FormatName { get; set; }

        /// <summary>
        /// Gets or sets the format_long_name.
        /// </summary>
        /// <value>The format_long_name.</value>
        [JsonPropertyName("format_long_name")]
        public string FormatLongName { get; set; }

        /// <summary>
        /// Gets or sets the start_time.
        /// </summary>
        /// <value>The start_time.</value>
        [JsonPropertyName("start_time")]
        public string StartTime { get; set; }

        /// <summary>
        /// Gets or sets the duration.
        /// </summary>
        /// <value>The duration.</value>
        [JsonPropertyName("duration")]
        public string Duration { get; set; }

        /// <summary>
        /// Gets or sets the size.
        /// </summary>
        /// <value>The size.</value>
        [JsonPropertyName("size")]
        public string Size { get; set; }

        /// <summary>
        /// Gets or sets the bit_rate.
        /// </summary>
        /// <value>The bit_rate.</value>
        [JsonPropertyName("bit_rate")]
        public string BitRate { get; set; }

        /// <summary>
        /// Gets or sets the probe_score.
        /// </summary>
        /// <value>The probe_score.</value>
        [JsonPropertyName("probe_score")]
        public int ProbeScore { get; set; }

        /// <summary>
        /// Gets or sets the tags.
        /// </summary>
        /// <value>The tags.</value>
        [JsonPropertyName("tags")]
        public IReadOnlyDictionary<string, string> Tags { get; set; }
    }
}


# Probing/MediaChapter.cs
#nullable disable
#pragma warning disable CS1591

using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace MediaBrowser.MediaEncoding.Probing
{
    /// <summary>
    /// Class MediaChapter.
    /// </summary>
    public class MediaChapter
    {
        [JsonPropertyName("id")]
        public long Id { get; set; }

        [JsonPropertyName("time_base")]
        public string TimeBase { get; set; }

        [JsonPropertyName("start")]
        public long Start { get; set; }

        [JsonPropertyName("start_time")]
        public string StartTime { get; set; }

        [JsonPropertyName("end")]
        public long End { get; set; }

        [JsonPropertyName("end_time")]
        public string EndTime { get; set; }

        [JsonPropertyName("tags")]
        public IReadOnlyDictionary<string, string> Tags { get; set; }
    }
}


# Probing/InternalMediaInfoResult.cs
#nullable disable

using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace MediaBrowser.MediaEncoding.Probing
{
    /// <summary>
    /// Class MediaInfoResult.
    /// </summary>
    public class InternalMediaInfoResult
    {
        /// <summary>
        /// Gets or sets the streams.
        /// </summary>
        /// <value>The streams.</value>
        [JsonPropertyName("streams")]
        public IReadOnlyList<MediaStreamInfo> Streams { get; set; }

        /// <summary>
        /// Gets or sets the format.
        /// </summary>
        /// <value>The format.</value>
        [JsonPropertyName("format")]
        public MediaFormatInfo Format { get; set; }

        /// <summary>
        /// Gets or sets the chapters.
        /// </summary>
        /// <value>The chapters.</value>
        [JsonPropertyName("chapters")]
        public IReadOnlyList<MediaChapter> Chapters { get; set; }

        /// <summary>
        /// Gets or sets the frames.
        /// </summary>
        /// <value>The streams.</value>
        [JsonPropertyName("frames")]
        public IReadOnlyList<MediaFrameInfo> Frames { get; set; }
    }
}


# Probing/MediaStreamInfoSideData.cs
using System.Text.Json.Serialization;

namespace MediaBrowser.MediaEncoding.Probing
{
    /// <summary>
    /// Class MediaStreamInfoSideData.
    /// </summary>
    public class MediaStreamInfoSideData
    {
        /// <summary>
        /// Gets or sets the SideDataType.
        /// </summary>
        /// <value>The SideDataType.</value>
        [JsonPropertyName("side_data_type")]
        public string? SideDataType { get; set; }

        /// <summary>
        /// Gets or sets the DvVersionMajor.
        /// </summary>
        /// <value>The DvVersionMajor.</value>
        [JsonPropertyName("dv_version_major")]
        public int? DvVersionMajor { get; set; }

        /// <summary>
        /// Gets or sets the DvVersionMinor.
        /// </summary>
        /// <value>The DvVersionMinor.</value>
        [JsonPropertyName("dv_version_minor")]
        public int? DvVersionMinor { get; set; }

        /// <summary>
        /// Gets or sets the DvProfile.
        /// </summary>
        /// <value>The DvProfile.</value>
        [JsonPropertyName("dv_profile")]
        public int? DvProfile { get; set; }

        /// <summary>
        /// Gets or sets the DvLevel.
        /// </summary>
        /// <value>The DvLevel.</value>
        [JsonPropertyName("dv_level")]
        public int? DvLevel { get; set; }

        /// <summary>
        /// Gets or sets the RpuPresentFlag.
        /// </summary>
        /// <value>The RpuPresentFlag.</value>
        [JsonPropertyName("rpu_present_flag")]
        public int? RpuPresentFlag { get; set; }

        /// <summary>
        /// Gets or sets the ElPresentFlag.
        /// </summary>
        /// <value>The ElPresentFlag.</value>
        [JsonPropertyName("el_present_flag")]
        public int? ElPresentFlag { get; set; }

        /// <summary>
        /// Gets or sets the BlPresentFlag.
        /// </summary>
        /// <value>The BlPresentFlag.</value>
        [JsonPropertyName("bl_present_flag")]
        public int? BlPresentFlag { get; set; }

        /// <summary>
        /// Gets or sets the DvBlSignalCompatibilityId.
        /// </summary>
        /// <value>The DvBlSignalCompatibilityId.</value>
        [JsonPropertyName("dv_bl_signal_compatibility_id")]
        public int? DvBlSignalCompatibilityId { get; set; }

        /// <summary>
        /// Gets or sets the Rotation in degrees.
        /// </summary>
        /// <value>The Rotation.</value>
        [JsonPropertyName("rotation")]
        public int? Rotation { get; set; }
    }
}


# Encoder/EncoderValidator.cs
#pragma warning disable CS1591

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using System.Runtime.Versioning;
using System.Text.RegularExpressions;
using MediaBrowser.Controller.MediaEncoding;
using Microsoft.Extensions.Logging;

namespace MediaBrowser.MediaEncoding.Encoder
{
    public partial class EncoderValidator
    {
        private static readonly string[] _requiredDecoders =
        [
            "h264",
            "hevc",
            "vp8",
            "libvpx",
            "vp9",
            "libvpx-vp9",
            "av1",
            "libdav1d",
            "mpeg2video",
            "mpeg4",
            "msmpeg4",
            "dca",
            "ac3",
            "ac4",
            "aac",
            "mp3",
            "flac",
            "truehd",
            "h264_qsv",
            "hevc_qsv",
            "mpeg2_qsv",
            "vc1_qsv",
            "vp8_qsv",
            "vp9_qsv",
            "av1_qsv",
            "h264_cuvid",
            "hevc_cuvid",
            "mpeg2_cuvid",
            "vc1_cuvid",
            "mpeg4_cuvid",
            "vp8_cuvid",
            "vp9_cuvid",
            "av1_cuvid",
            "h264_rkmpp",
            "hevc_rkmpp",
            "mpeg1_rkmpp",
            "mpeg2_rkmpp",
            "mpeg4_rkmpp",
            "vp8_rkmpp",
            "vp9_rkmpp",
            "av1_rkmpp"
        ];

        private static readonly string[] _requiredEncoders =
        [
            "libx264",
            "libx265",
            "libsvtav1",
            "aac",
            "aac_at",
            "libfdk_aac",
            "ac3",
            "alac",
            "dca",
            "libmp3lame",
            "libopus",
            "libvorbis",
            "flac",
            "truehd",
            "srt",
            "h264_amf",
            "hevc_amf",
            "av1_amf",
            "h264_qsv",
            "hevc_qsv",
            "mjpeg_qsv",
            "av1_qsv",
            "h264_nvenc",
            "hevc_nvenc",
            "av1_nvenc",
            "h264_vaapi",
            "hevc_vaapi",
            "av1_vaapi",
            "mjpeg_vaapi",
            "h264_v4l2m2m",
            "h264_videotoolbox",
            "hevc_videotoolbox",
            "mjpeg_videotoolbox",
            "h264_rkmpp",
            "hevc_rkmpp",
            "mjpeg_rkmpp"
        ];

        private static readonly string[] _requiredFilters =
        [
            // sw
            "alphasrc",
            "zscale",
            "tonemapx",
            // qsv
            "scale_qsv",
            "vpp_qsv",
            "deinterlace_qsv",
            "overlay_qsv",
            // cuda
            "scale_cuda",
            "yadif_cuda",
            "bwdif_cuda",
            "tonemap_cuda",
            "overlay_cuda",
            "transpose_cuda",
            "hwupload_cuda",
            // opencl
            "scale_opencl",
            "tonemap_opencl",
            "overlay_opencl",
            "transpose_opencl",
            "yadif_opencl",
            "bwdif_opencl",
            // vaapi
            "scale_vaapi",
            "deinterlace_vaapi",
            "tonemap_vaapi",
            "procamp_vaapi",
            "overlay_vaapi",
            "transpose_vaapi",
            "hwupload_vaapi",
            // vulkan
            "libplacebo",
            "scale_vulkan",
            "overlay_vulkan",
            "transpose_vulkan",
            "flip_vulkan",
            // videotoolbox
            "yadif_videotoolbox",
            "bwdif_videotoolbox",
            "scale_vt",
            "transpose_vt",
            "overlay_videotoolbox",
            "tonemap_videotoolbox",
            // rkrga
            "scale_rkrga",
            "vpp_rkrga",
            "overlay_rkrga"
        ];

        private static readonly Dictionary<FilterOptionType, (string, string)> _filterOptionsDict = new Dictionary<FilterOptionType, (string, string)>
        {
            { FilterOptionType.ScaleCudaFormat, ("scale_cuda", "format") },
            { FilterOptionType.TonemapCudaName, ("tonemap_cuda", "GPU accelerated HDR to SDR tonemapping") },
            { FilterOptionType.TonemapOpenclBt2390, ("tonemap_opencl", "bt2390") },
            { FilterOptionType.OverlayOpenclFrameSync, ("overlay_opencl", "Action to take when encountering EOF from secondary input") },
            { FilterOptionType.OverlayVaapiFrameSync, ("overlay_vaapi", "Action to take when encountering EOF from secondary input") },
            { FilterOptionType.OverlayVulkanFrameSync, ("overlay_vulkan", "Action to take when encountering EOF from secondary input") },
            { FilterOptionType.TransposeOpenclReversal, ("transpose_opencl", "rotate by half-turn") },
            { FilterOptionType.OverlayOpenclAlphaFormat, ("overlay_opencl", "alpha_format") },
            { FilterOptionType.OverlayCudaAlphaFormat, ("overlay_cuda", "alpha_format") }
        };

        private static readonly Dictionary<BitStreamFilterOptionType, (string, string)> _bsfOptionsDict = new Dictionary<BitStreamFilterOptionType, (string, string)>
        {
            { BitStreamFilterOptionType.HevcMetadataRemoveDovi, ("hevc_metadata", "remove_dovi") },
            { BitStreamFilterOptionType.HevcMetadataRemoveHdr10Plus, ("hevc_metadata", "remove_hdr10plus") },
            { BitStreamFilterOptionType.Av1MetadataRemoveDovi, ("av1_metadata", "remove_dovi") },
            { BitStreamFilterOptionType.Av1MetadataRemoveHdr10Plus, ("av1_metadata", "remove_hdr10plus") },
            { BitStreamFilterOptionType.DoviRpuStrip, ("dovi_rpu", "strip") }
        };

        // These are the library versions that corresponds to our minimum ffmpeg version 4.4 according to the version table below
        // Refers to the versions in https://ffmpeg.org/download.html
        private static readonly Dictionary<string, Version> _ffmpegMinimumLibraryVersions = new Dictionary<string, Version>
        {
            { "libavutil", new Version(56, 70) },
            { "libavcodec", new Version(58, 134) },
            { "libavformat", new Version(58, 76) },
            { "libavdevice", new Version(58, 13) },
            { "libavfilter", new Version(7, 110) },
            { "libswscale", new Version(5, 9) },
            { "libswresample", new Version(3, 9) },
            { "libpostproc", new Version(55, 9) }
        };

        private readonly ILogger _logger;

        private readonly string _encoderPath;

        private readonly Version _minFFmpegMultiThreadedCli = new Version(7, 0);

        public EncoderValidator(ILogger logger, string encoderPath)
        {
            _logger = logger;
            _encoderPath = encoderPath;
        }

        private enum Codec
        {
            Encoder,
            Decoder
        }

        // When changing this, also change the minimum library versions in _ffmpegMinimumLibraryVersions
        public static Version MinVersion { get; } = new Version(4, 4);

        public static Version? MaxVersion { get; } = null;

        [GeneratedRegex(@"^ffmpeg version n?((?:[0-9]+\.?)+)")]
        private static partial Regex FfmpegVersionRegex();

        [GeneratedRegex(@"((?<name>lib\w+)\s+(?<major>[0-9]+)\.\s*(?<minor>[0-9]+))", RegexOptions.Multiline)]
        private static partial Regex LibraryRegex();

        public bool ValidateVersion()
        {
            string output;
            try
            {
                output = GetProcessOutput(_encoderPath, "-version", false, null);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error validating encoder");
                return false;
            }

            if (string.IsNullOrWhiteSpace(output))
            {
                _logger.LogError("FFmpeg validation: The process returned no result");
                return false;
            }

            _logger.LogDebug("ffmpeg output: {Output}", output);

            return ValidateVersionInternal(output);
        }

        internal bool ValidateVersionInternal(string versionOutput)
        {
            if (versionOutput.Contains("Libav developers", StringComparison.OrdinalIgnoreCase))
            {
                _logger.LogError("FFmpeg validation: avconv instead of ffmpeg is not supported");
                return false;
            }

            // Work out what the version under test is
            var version = GetFFmpegVersionInternal(versionOutput);

            _logger.LogInformation("Found ffmpeg version {Version}", version is not null ? version.ToString() : "unknown");

            if (version is null)
            {
                if (MaxVersion is not null) // Version is unknown
                {
                    if (MinVersion == MaxVersion)
                    {
                        _logger.LogWarning("FFmpeg validation: We recommend version {MinVersion}", MinVersion);
                    }
                    else
                    {
                        _logger.LogWarning("FFmpeg validation: We recommend a minimum of {MinVersion} and maximum of {MaxVersion}", MinVersion, MaxVersion);
                    }
                }
                else
                {
                    _logger.LogWarning("FFmpeg validation: We recommend minimum version {MinVersion}", MinVersion);
                }

                return false;
            }

            if (version < MinVersion) // Version is below what we recommend
            {
                _logger.LogWarning("FFmpeg validation: The minimum recommended version is {MinVersion}", MinVersion);
                return false;
            }

            if (MaxVersion is not null && version > MaxVersion) // Version is above what we recommend
            {
                _logger.LogWarning("FFmpeg validation: The maximum recommended version is {MaxVersion}", MaxVersion);
                return false;
            }

            return true;
        }

        public IEnumerable<string> GetDecoders() => GetCodecs(Codec.Decoder);

        public IEnumerable<string> GetEncoders() => GetCodecs(Codec.Encoder);

        public IEnumerable<string> GetHwaccels() => GetHwaccelTypes();

        public IEnumerable<string> GetFilters() => GetFFmpegFilters();

        public IDictionary<FilterOptionType, bool> GetFiltersWithOption() => _filterOptionsDict
            .ToDictionary(item => item.Key, item => CheckFilterWithOption(item.Value.Item1, item.Value.Item2));

        public IDictionary<BitStreamFilterOptionType, bool> GetBitStreamFiltersWithOption() => _bsfOptionsDict
            .ToDictionary(item => item.Key, item => CheckBitStreamFilterWithOption(item.Value.Item1, item.Value.Item2));

        public Version? GetFFmpegVersion()
        {
            string output;
            try
            {
                output = GetProcessOutput(_encoderPath, "-version", false, null);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error validating encoder");
                return null;
            }

            if (string.IsNullOrWhiteSpace(output))
            {
                _logger.LogError("FFmpeg validation: The process returned no result");
                return null;
            }

            _logger.LogDebug("ffmpeg output: {Output}", output);

            return GetFFmpegVersionInternal(output);
        }

        /// <summary>
        /// Using the output from "ffmpeg -version" work out the FFmpeg version.
        /// For pre-built binaries the first line should contain a string like "ffmpeg version x.y", which is easy
        /// to parse. If this is not available, then we try to match known library versions to FFmpeg versions.
        /// If that fails then we test the libraries to determine if they're newer than our minimum versions.
        /// </summary>
        /// <param name="output">The output from "ffmpeg -version".</param>
        /// <returns>The FFmpeg version.</returns>
        internal Version? GetFFmpegVersionInternal(string output)
        {
            // For pre-built binaries the FFmpeg version should be mentioned at the very start of the output
            var match = FfmpegVersionRegex().Match(output);

            if (match.Success)
            {
                if (Version.TryParse(match.Groups[1].ValueSpan, out var result))
                {
                    return result;
                }
            }

            var versionMap = GetFFmpegLibraryVersions(output);

            var allVersionsValidated = true;

            foreach (var minimumVersion in _ffmpegMinimumLibraryVersions)
            {
                if (versionMap.TryGetValue(minimumVersion.Key, out var foundVersion))
                {
                    if (foundVersion >= minimumVersion.Value)
                    {
                        _logger.LogInformation("Found {Library} version {FoundVersion} ({MinimumVersion})", minimumVersion.Key, foundVersion, minimumVersion.Value);
                    }
                    else
                    {
                        _logger.LogWarning("Found {Library} version {FoundVersion} lower than recommended version {MinimumVersion}", minimumVersion.Key, foundVersion, minimumVersion.Value);
                        allVersionsValidated = false;
                    }
                }
                else
                {
                    _logger.LogError("{Library} version not found", minimumVersion.Key);
                    allVersionsValidated = false;
                }
            }

            return allVersionsValidated ? MinVersion : null;
        }

        /// <summary>
        /// Grabs the library names and major.minor version numbers from the 'ffmpeg -version' output
        /// and condenses them on to one line.  Output format is "name1=major.minor,name2=major.minor,etc.".
        /// </summary>
        /// <param name="output">The 'ffmpeg -version' output.</param>
        /// <returns>The library names and major.minor version numbers.</returns>
        private static Dictionary<string, Version> GetFFmpegLibraryVersions(string output)
        {
            var map = new Dictionary<string, Version>();

            foreach (Match match in LibraryRegex().Matches(output))
            {
                var version = new Version(
                    int.Parse(match.Groups["major"].ValueSpan, CultureInfo.InvariantCulture),
                    int.Parse(match.Groups["minor"].ValueSpan, CultureInfo.InvariantCulture));

                map.Add(match.Groups["name"].Value, version);
            }

            return map;
        }

        public bool CheckVaapiDeviceByDriverName(string driverName, string renderNodePath)
        {
            if (!OperatingSystem.IsLinux())
            {
                return false;
            }

            if (string.IsNullOrEmpty(driverName) || string.IsNullOrEmpty(renderNodePath))
            {
                return false;
            }

            try
            {
                var output = GetProcessOutput(_encoderPath, "-v verbose -hide_banner -init_hw_device vaapi=va:" + renderNodePath, true, null);
                return output.Contains(driverName, StringComparison.Ordinal);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error detecting the given vaapi render node path");
                return false;
            }
        }

        public bool CheckVulkanDrmDeviceByExtensionName(string renderNodePath, string[] vulkanExtensions)
        {
            if (!OperatingSystem.IsLinux())
            {
                return false;
            }

            if (string.IsNullOrEmpty(renderNodePath))
            {
                return false;
            }

            try
            {
                var command = "-v verbose -hide_banner -init_hw_device drm=dr:" + renderNodePath + " -init_hw_device vulkan=vk@dr";
                var output = GetProcessOutput(_encoderPath, command, true, null);
                foreach (string ext in vulkanExtensions)
                {
                    if (!output.Contains(ext, StringComparison.Ordinal))
                    {
                        return false;
                    }
                }

                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error detecting the given drm render node path");
                return false;
            }
        }

        [SupportedOSPlatform("macos")]
        public bool CheckIsVideoToolboxAv1DecodeAvailable()
        {
            return ApplePlatformHelper.HasAv1HardwareAccel(_logger);
        }

        private IEnumerable<string> GetHwaccelTypes()
        {
            string? output = null;
            try
            {
                output = GetProcessOutput(_encoderPath, "-hwaccels", false, null);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error detecting available hwaccel types");
            }

            if (string.IsNullOrWhiteSpace(output))
            {
                return [];
            }

            var found = output.Split(['\r', '\n'], StringSplitOptions.RemoveEmptyEntries).Skip(1).Distinct().ToList();
            _logger.LogInformation("Available hwaccel types: {Types}", found);

            return found;
        }

        public bool CheckFilterWithOption(string filter, string option)
        {
            if (string.IsNullOrEmpty(filter) || string.IsNullOrEmpty(option))
            {
                return false;
            }

            string output;
            try
            {
                output = GetProcessOutput(_encoderPath, "-h filter=" + filter, false, null);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error detecting the given filter");
                return false;
            }

            if (output.Contains("Filter " + filter, StringComparison.Ordinal))
            {
                return output.Contains(option, StringComparison.Ordinal);
            }

            _logger.LogWarning("Filter: {Name} with option {Option} is not available", filter, option);

            return false;
        }

        public bool CheckBitStreamFilterWithOption(string filter, string option)
        {
            if (string.IsNullOrEmpty(filter) || string.IsNullOrEmpty(option))
            {
                return false;
            }

            string output;
            try
            {
                output = GetProcessOutput(_encoderPath, "-h bsf=" + filter, false, null);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error detecting the given bit stream filter");
                return false;
            }

            if (output.Contains("Bit stream filter " + filter, StringComparison.Ordinal))
            {
                return output.Contains(option, StringComparison.Ordinal);
            }

            _logger.LogWarning("Bit stream filter: {Name} with option {Option} is not available", filter, option);

            return false;
        }

        public bool CheckSupportedRuntimeKey(string keyDesc, Version? ffmpegVersion)
        {
            if (string.IsNullOrEmpty(keyDesc))
            {
                return false;
            }

            string output;
            try
            {
                // With multi-threaded cli support, FFmpeg 7 is less sensitive to keyboard input
                var duration = ffmpegVersion >= _minFFmpegMultiThreadedCli ? 10000 : 1000;
                output = GetProcessOutput(_encoderPath, $"-hide_banner -f lavfi -i nullsrc=s=1x1:d={duration} -f null -", true, "?");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error checking supported runtime key");
                return false;
            }

            return output.Contains(keyDesc, StringComparison.Ordinal);
        }

        public bool CheckSupportedHwaccelFlag(string flag)
        {
            return !string.IsNullOrEmpty(flag) && GetProcessExitCode(_encoderPath, $"-loglevel quiet -hwaccel_flags +{flag} -hide_banner -f lavfi -i nullsrc=s=1x1:d=100 -f null -");
        }

        public bool CheckSupportedProberOption(string option, string proberPath)
        {
            return !string.IsNullOrEmpty(option) && GetProcessExitCode(proberPath, $"-loglevel quiet -f lavfi -i nullsrc=s=1x1:d=1 -{option}");
        }

        private IEnumerable<string> GetCodecs(Codec codec)
        {
            string codecstr = codec == Codec.Encoder ? "encoders" : "decoders";
            string output;
            try
            {
                output = GetProcessOutput(_encoderPath, "-" + codecstr, false, null);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error detecting available {Codec}", codecstr);
                return [];
            }

            if (string.IsNullOrWhiteSpace(output))
            {
                return [];
            }

            var required = codec == Codec.Encoder ? _requiredEncoders : _requiredDecoders;

            var found = CodecRegex()
                .Matches(output)
                .Select(x => x.Groups["codec"].Value)
                .Where(x => required.Contains(x));

            _logger.LogInformation("Available {Codec}: {Codecs}", codecstr, found);

            return found;
        }

        private IEnumerable<string> GetFFmpegFilters()
        {
            string output;
            try
            {
                output = GetProcessOutput(_encoderPath, "-filters", false, null);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error detecting available filters");
                return [];
            }

            if (string.IsNullOrWhiteSpace(output))
            {
                return [];
            }

            var found = FilterRegex()
                .Matches(output)
                .Select(x => x.Groups["filter"].Value)
                .Where(x => _requiredFilters.Contains(x));

            _logger.LogInformation("Available filters: {Filters}", found);

            return found;
        }

        private string GetProcessOutput(string path, string arguments, bool readStdErr, string? testKey)
        {
            var redirectStandardIn = !string.IsNullOrEmpty(testKey);
            using (var process = new Process
            {
                StartInfo = new ProcessStartInfo(path, arguments)
                {
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    WindowStyle = ProcessWindowStyle.Hidden,
                    ErrorDialog = false,
                    RedirectStandardInput = redirectStandardIn,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true
                }
            })
            {
                _logger.LogDebug("Running {Path} {Arguments}", path, arguments);

                process.Start();

                if (redirectStandardIn)
                {
                    using var writer = process.StandardInput;
                    writer.Write(testKey);
                }

                using var reader = readStdErr ? process.StandardError : process.StandardOutput;
                return reader.ReadToEnd();
            }
        }

        private bool GetProcessExitCode(string path, string arguments)
        {
            using var process = new Process();
            process.StartInfo = new ProcessStartInfo(path, arguments)
            {
                CreateNoWindow = true,
                UseShellExecute = false,
                WindowStyle = ProcessWindowStyle.Hidden,
                ErrorDialog = false
            };
            _logger.LogDebug("Running {Path} {Arguments}", path, arguments);

            try
            {
                process.Start();
                process.WaitForExit();
                return process.ExitCode == 0;
            }
            catch (Exception ex)
            {
                _logger.LogError("Running {Path} {Arguments} failed with exception {Exception}", path, arguments, ex.Message);
                return false;
            }
        }

        [GeneratedRegex("^\\s\\S{6}\\s(?<codec>[\\w|-]+)\\s+.+$", RegexOptions.Multiline)]
        private static partial Regex CodecRegex();

        [GeneratedRegex("^\\s\\S{3}\\s(?<filter>[\\w|-]+)\\s+.+$", RegexOptions.Multiline)]
        private static partial Regex FilterRegex();
    }
}


# Encoder/MediaEncoder.cs
#nullable disable
#pragma warning disable CS1591

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using AsyncKeyedLock;
using Jellyfin.Data.Enums;
using Jellyfin.Extensions;
using Jellyfin.Extensions.Json;
using Jellyfin.Extensions.Json.Converters;
using MediaBrowser.Common;
using MediaBrowser.Common.Configuration;
using MediaBrowser.Common.Extensions;
using MediaBrowser.Controller.Configuration;
using MediaBrowser.Controller.Extensions;
using MediaBrowser.Controller.MediaEncoding;
using MediaBrowser.MediaEncoding.Probing;
using MediaBrowser.Model.Configuration;
using MediaBrowser.Model.Dlna;
using MediaBrowser.Model.Drawing;
using MediaBrowser.Model.Dto;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.Globalization;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.MediaInfo;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace MediaBrowser.MediaEncoding.Encoder
{
    /// <summary>
    /// Class MediaEncoder.
    /// </summary>
    public partial class MediaEncoder : IMediaEncoder, IDisposable
    {
        /// <summary>
        /// The default SDR image extraction timeout in milliseconds.
        /// </summary>
        internal const int DefaultSdrImageExtractionTimeout = 10000;

        /// <summary>
        /// The default HDR image extraction timeout in milliseconds.
        /// </summary>
        internal const int DefaultHdrImageExtractionTimeout = 20000;

        private readonly ILogger<MediaEncoder> _logger;
        private readonly IServerConfigurationManager _configurationManager;
        private readonly IFileSystem _fileSystem;
        private readonly ILocalizationManager _localization;
        private readonly IBlurayExaminer _blurayExaminer;
        private readonly IConfiguration _config;
        private readonly IServerConfigurationManager _serverConfig;
        private readonly string _startupOptionFFmpegPath;

        private readonly AsyncNonKeyedLocker _thumbnailResourcePool;

        private readonly Lock _runningProcessesLock = new();
        private readonly List<ProcessWrapper> _runningProcesses = new List<ProcessWrapper>();

        // MediaEncoder is registered as a Singleton
        private readonly JsonSerializerOptions _jsonSerializerOptions;

        private List<string> _encoders = new List<string>();
        private List<string> _decoders = new List<string>();
        private List<string> _hwaccels = new List<string>();
        private List<string> _filters = new List<string>();
        private IDictionary<FilterOptionType, bool> _filtersWithOption = new Dictionary<FilterOptionType, bool>();
        private IDictionary<BitStreamFilterOptionType, bool> _bitStreamFiltersWithOption = new Dictionary<BitStreamFilterOptionType, bool>();

        private bool _isPkeyPauseSupported = false;
        private bool _isLowPriorityHwDecodeSupported = false;
        private bool _proberSupportsFirstVideoFrame = false;

        private bool _isVaapiDeviceAmd = false;
        private bool _isVaapiDeviceInteliHD = false;
        private bool _isVaapiDeviceInteli965 = false;
        private bool _isVaapiDeviceSupportVulkanDrmModifier = false;
        private bool _isVaapiDeviceSupportVulkanDrmInterop = false;

        private bool _isVideoToolboxAv1DecodeAvailable = false;

        private static string[] _vulkanImageDrmFmtModifierExts =
        {
            "VK_EXT_image_drm_format_modifier",
        };

        private static string[] _vulkanExternalMemoryDmaBufExts =
        {
            "VK_KHR_external_memory_fd",
            "VK_EXT_external_memory_dma_buf",
            "VK_KHR_external_semaphore_fd",
            "VK_EXT_external_memory_host"
        };

        private Version _ffmpegVersion = null;
        private string _ffmpegPath = string.Empty;
        private string _ffprobePath;
        private int _threads;

        public MediaEncoder(
            ILogger<MediaEncoder> logger,
            IServerConfigurationManager configurationManager,
            IFileSystem fileSystem,
            IBlurayExaminer blurayExaminer,
            ILocalizationManager localization,
            IConfiguration config,
            IServerConfigurationManager serverConfig)
        {
            _logger = logger;
            _configurationManager = configurationManager;
            _fileSystem = fileSystem;
            _blurayExaminer = blurayExaminer;
            _localization = localization;
            _config = config;
            _serverConfig = serverConfig;
            _startupOptionFFmpegPath = config.GetValue<string>(Controller.Extensions.ConfigurationExtensions.FfmpegPathKey) ?? string.Empty;

            _jsonSerializerOptions = new JsonSerializerOptions(JsonDefaults.Options);
            _jsonSerializerOptions.Converters.Add(new JsonBoolStringConverter());

            // Although the type is not nullable, this might still be null during unit tests
            var semaphoreCount = serverConfig.Configuration?.ParallelImageEncodingLimit ?? 0;
            if (semaphoreCount < 1)
            {
                semaphoreCount = Environment.ProcessorCount;
            }

            _thumbnailResourcePool = new(semaphoreCount);
        }

        /// <inheritdoc />
        public string EncoderPath => _ffmpegPath;

        /// <inheritdoc />
        public string ProbePath => _ffprobePath;

        /// <inheritdoc />
        public Version EncoderVersion => _ffmpegVersion;

        /// <inheritdoc />
        public bool IsPkeyPauseSupported => _isPkeyPauseSupported;

        /// <inheritdoc />
        public bool IsVaapiDeviceAmd => _isVaapiDeviceAmd;

        /// <inheritdoc />
        public bool IsVaapiDeviceInteliHD => _isVaapiDeviceInteliHD;

        /// <inheritdoc />
        public bool IsVaapiDeviceInteli965 => _isVaapiDeviceInteli965;

        /// <inheritdoc />
        public bool IsVaapiDeviceSupportVulkanDrmModifier => _isVaapiDeviceSupportVulkanDrmModifier;

        /// <inheritdoc />
        public bool IsVaapiDeviceSupportVulkanDrmInterop => _isVaapiDeviceSupportVulkanDrmInterop;

        public bool IsVideoToolboxAv1DecodeAvailable => _isVideoToolboxAv1DecodeAvailable;

        [GeneratedRegex(@"[^\/\\]+?(\.[^\/\\\n.]+)?$")]
        private static partial Regex FfprobePathRegex();

        /// <summary>
        /// Run at startup to validate ffmpeg.
        /// Sets global variables FFmpegPath.
        /// Precedence is: CLI/Env var > Config > $PATH.
        /// </summary>
        /// <returns>bool indicates whether a valid ffmpeg is found.</returns>
        public bool SetFFmpegPath()
        {
            var skipValidation = _config.GetFFmpegSkipValidation();
            if (skipValidation)
            {
                _logger.LogWarning("FFmpeg: Skipping FFmpeg Validation due to FFmpeg:novalidation set to true");
                return true;
            }

            // 1) Check if the --ffmpeg CLI switch has been given
            var ffmpegPath = _startupOptionFFmpegPath;
            string ffmpegPathSetMethodText = "command line or environment variable";
            if (string.IsNullOrEmpty(ffmpegPath))
            {
                // 2) Custom path stored in config/encoding xml file under tag <EncoderAppPath> should be used as a fallback
                ffmpegPath = _configurationManager.GetEncodingOptions().EncoderAppPath;
                ffmpegPathSetMethodText = "encoding.xml config file";
                if (string.IsNullOrEmpty(ffmpegPath))
                {
                    // 3) Check "ffmpeg"
                    ffmpegPath = "ffmpeg";
                    ffmpegPathSetMethodText = "system $PATH";
                }
            }

            if (!ValidatePath(ffmpegPath))
            {
                _ffmpegPath = null;
                _logger.LogError("FFmpeg: Path set by {FfmpegPathSetMethodText} is invalid", ffmpegPathSetMethodText);
                return false;
            }

            // Write the FFmpeg path to the config/encoding.xml file as <EncoderAppPathDisplay> so it appears in UI
            var options = _configurationManager.GetEncodingOptions();
            options.EncoderAppPathDisplay = _ffmpegPath ?? string.Empty;
            _configurationManager.SaveConfiguration("encoding", options);

            // Only if mpeg path is set, try and set path to probe
            if (_ffmpegPath is not null)
            {
                // Determine a probe path from the mpeg path
                _ffprobePath = FfprobePathRegex().Replace(_ffmpegPath, "ffprobe$1");

                // Interrogate to understand what coders are supported
                var validator = new EncoderValidator(_logger, _ffmpegPath);

                SetAvailableDecoders(validator.GetDecoders());
                SetAvailableEncoders(validator.GetEncoders());
                SetAvailableFilters(validator.GetFilters());
                SetAvailableFiltersWithOption(validator.GetFiltersWithOption());
                SetAvailableBitStreamFiltersWithOption(validator.GetBitStreamFiltersWithOption());
                SetAvailableHwaccels(validator.GetHwaccels());
                SetMediaEncoderVersion(validator);

                _threads = EncodingHelper.GetNumberOfThreads(null, options, null);

                _isPkeyPauseSupported = validator.CheckSupportedRuntimeKey("p      pause transcoding", _ffmpegVersion);
                _isLowPriorityHwDecodeSupported = validator.CheckSupportedHwaccelFlag("low_priority");
                _proberSupportsFirstVideoFrame = validator.CheckSupportedProberOption("only_first_vframe", _ffprobePath);

                // Check the Vaapi device vendor
                if (OperatingSystem.IsLinux()
                    && SupportsHwaccel("vaapi")
                    && !string.IsNullOrEmpty(options.VaapiDevice)
                    && options.HardwareAccelerationType == HardwareAccelerationType.vaapi)
                {
                    _isVaapiDeviceAmd = validator.CheckVaapiDeviceByDriverName("Mesa Gallium driver", options.VaapiDevice);
                    _isVaapiDeviceInteliHD = validator.CheckVaapiDeviceByDriverName("Intel iHD driver", options.VaapiDevice);
                    _isVaapiDeviceInteli965 = validator.CheckVaapiDeviceByDriverName("Intel i965 driver", options.VaapiDevice);
                    _isVaapiDeviceSupportVulkanDrmModifier = validator.CheckVulkanDrmDeviceByExtensionName(options.VaapiDevice, _vulkanImageDrmFmtModifierExts);
                    _isVaapiDeviceSupportVulkanDrmInterop = validator.CheckVulkanDrmDeviceByExtensionName(options.VaapiDevice, _vulkanExternalMemoryDmaBufExts);

                    if (_isVaapiDeviceAmd)
                    {
                        _logger.LogInformation("VAAPI device {RenderNodePath} is AMD GPU", options.VaapiDevice);
                    }
                    else if (_isVaapiDeviceInteliHD)
                    {
                        _logger.LogInformation("VAAPI device {RenderNodePath} is Intel GPU (iHD)", options.VaapiDevice);
                    }
                    else if (_isVaapiDeviceInteli965)
                    {
                        _logger.LogInformation("VAAPI device {RenderNodePath} is Intel GPU (i965)", options.VaapiDevice);
                    }

                    if (_isVaapiDeviceSupportVulkanDrmModifier)
                    {
                        _logger.LogInformation("VAAPI device {RenderNodePath} supports Vulkan DRM modifier", options.VaapiDevice);
                    }

                    if (_isVaapiDeviceSupportVulkanDrmInterop)
                    {
                        _logger.LogInformation("VAAPI device {RenderNodePath} supports Vulkan DRM interop", options.VaapiDevice);
                    }
                }

                // Check if VideoToolbox supports AV1 decode
                if (OperatingSystem.IsMacOS() && SupportsHwaccel("videotoolbox"))
                {
                    _isVideoToolboxAv1DecodeAvailable = validator.CheckIsVideoToolboxAv1DecodeAvailable();
                }
            }

            _logger.LogInformation("FFmpeg: {FfmpegPath}", _ffmpegPath ?? string.Empty);
            return !string.IsNullOrWhiteSpace(ffmpegPath);
        }

        /// <summary>
        /// Validates the supplied FQPN to ensure it is a ffmpeg utility.
        /// If checks pass, global variable FFmpegPath is updated.
        /// </summary>
        /// <param name="path">FQPN to test.</param>
        /// <returns><c>true</c> if the version validation succeeded; otherwise, <c>false</c>.</returns>
        private bool ValidatePath(string path)
        {
            if (string.IsNullOrEmpty(path))
            {
                return false;
            }

            bool rc = new EncoderValidator(_logger, path).ValidateVersion();
            if (!rc)
            {
                _logger.LogError("FFmpeg: Failed version check: {Path}", path);
                return false;
            }

            _ffmpegPath = path;
            return true;
        }

        private string GetEncoderPathFromDirectory(string path, string filename, bool recursive = false)
        {
            try
            {
                var files = _fileSystem.GetFilePaths(path, recursive);

                return files.FirstOrDefault(i => Path.GetFileNameWithoutExtension(i.AsSpan()).Equals(filename, StringComparison.OrdinalIgnoreCase)
                                                    && !Path.GetExtension(i.AsSpan()).Equals(".c", StringComparison.OrdinalIgnoreCase));
            }
            catch (Exception)
            {
                // Trap all exceptions, like DirNotExists, and return null
                return null;
            }
        }

        public void SetAvailableEncoders(IEnumerable<string> list)
        {
            _encoders = list.ToList();
        }

        public void SetAvailableDecoders(IEnumerable<string> list)
        {
            _decoders = list.ToList();
        }

        public void SetAvailableHwaccels(IEnumerable<string> list)
        {
            _hwaccels = list.ToList();
        }

        public void SetAvailableFilters(IEnumerable<string> list)
        {
            _filters = list.ToList();
        }

        public void SetAvailableFiltersWithOption(IDictionary<FilterOptionType, bool> dict)
        {
            _filtersWithOption = dict;
        }

        public void SetAvailableBitStreamFiltersWithOption(IDictionary<BitStreamFilterOptionType, bool> dict)
        {
            _bitStreamFiltersWithOption = dict;
        }

        public void SetMediaEncoderVersion(EncoderValidator validator)
        {
            _ffmpegVersion = validator.GetFFmpegVersion();
        }

        /// <inheritdoc />
        public bool SupportsEncoder(string encoder)
        {
            return _encoders.Contains(encoder, StringComparer.OrdinalIgnoreCase);
        }

        /// <inheritdoc />
        public bool SupportsDecoder(string decoder)
        {
            return _decoders.Contains(decoder, StringComparer.OrdinalIgnoreCase);
        }

        /// <inheritdoc />
        public bool SupportsHwaccel(string hwaccel)
        {
            return _hwaccels.Contains(hwaccel, StringComparer.OrdinalIgnoreCase);
        }

        /// <inheritdoc />
        public bool SupportsFilter(string filter)
        {
            return _filters.Contains(filter, StringComparer.OrdinalIgnoreCase);
        }

        /// <inheritdoc />
        public bool SupportsFilterWithOption(FilterOptionType option)
        {
            return _filtersWithOption.TryGetValue(option, out var val) && val;
        }

        public bool SupportsBitStreamFilterWithOption(BitStreamFilterOptionType option)
        {
            return _bitStreamFiltersWithOption.TryGetValue(option, out var val) && val;
        }

        public bool CanEncodeToAudioCodec(string codec)
        {
            if (string.Equals(codec, "opus", StringComparison.OrdinalIgnoreCase))
            {
                codec = "libopus";
            }
            else if (string.Equals(codec, "mp3", StringComparison.OrdinalIgnoreCase))
            {
                codec = "libmp3lame";
            }

            return SupportsEncoder(codec);
        }

        public bool CanEncodeToSubtitleCodec(string codec)
        {
            // TODO
            return true;
        }

        /// <inheritdoc />
        public Task<MediaInfo> GetMediaInfo(MediaInfoRequest request, CancellationToken cancellationToken)
        {
            var extractChapters = request.MediaType == DlnaProfileType.Video && request.ExtractChapters;
            var extraArgs = GetExtraArguments(request);

            return GetMediaInfoInternal(
                GetInputArgument(request.MediaSource.Path, request.MediaSource),
                request.MediaSource.Path,
                request.MediaSource.Protocol,
                extractChapters,
                extraArgs,
                request.MediaType == DlnaProfileType.Audio,
                request.MediaSource.VideoType,
                cancellationToken);
        }

        internal string GetExtraArguments(MediaInfoRequest request)
        {
            var ffmpegAnalyzeDuration = _config.GetFFmpegAnalyzeDuration() ?? string.Empty;
            var ffmpegProbeSize = _config.GetFFmpegProbeSize() ?? string.Empty;
            var analyzeDuration = string.Empty;
            var extraArgs = string.Empty;

            if (request.MediaSource.AnalyzeDurationMs > 0)
            {
                analyzeDuration = "-analyzeduration " + (request.MediaSource.AnalyzeDurationMs * 1000);
            }
            else if (!string.IsNullOrEmpty(ffmpegAnalyzeDuration))
            {
                analyzeDuration = "-analyzeduration " + ffmpegAnalyzeDuration;
            }

            if (!string.IsNullOrEmpty(analyzeDuration))
            {
                extraArgs = analyzeDuration;
            }

            if (!string.IsNullOrEmpty(ffmpegProbeSize))
            {
                extraArgs += " -probesize " + ffmpegProbeSize;
            }

            if (request.MediaSource.RequiredHttpHeaders.TryGetValue("User-Agent", out var userAgent))
            {
                extraArgs += $" -user_agent \"{userAgent}\"";
            }

            if (request.MediaSource.Protocol == MediaProtocol.Rtsp)
            {
                extraArgs += " -rtsp_transport tcp+udp -rtsp_flags prefer_tcp";
            }

            return extraArgs;
        }

        /// <inheritdoc />
        public string GetInputArgument(IReadOnlyList<string> inputFiles, MediaSourceInfo mediaSource)
        {
            return EncodingUtils.GetInputArgument("file", inputFiles, mediaSource.Protocol);
        }

        /// <inheritdoc />
        public string GetInputArgument(string inputFile, MediaSourceInfo mediaSource)
        {
            var prefix = "file";
            if (mediaSource.IsoType == IsoType.BluRay)
            {
                prefix = "bluray";
            }

            return EncodingUtils.GetInputArgument(prefix, new[] { inputFile }, mediaSource.Protocol);
        }

        /// <inheritdoc />
        public string GetExternalSubtitleInputArgument(string inputFile)
        {
            const string Prefix = "file";

            return EncodingUtils.GetInputArgument(Prefix, new[] { inputFile }, MediaProtocol.File);
        }

        /// <summary>
        /// Gets the media info internal.
        /// </summary>
        /// <returns>Task{MediaInfoResult}.</returns>
        private async Task<MediaInfo> GetMediaInfoInternal(
            string inputPath,
            string primaryPath,
            MediaProtocol protocol,
            bool extractChapters,
            string probeSizeArgument,
            bool isAudio,
            VideoType? videoType,
            CancellationToken cancellationToken)
        {
            var args = extractChapters
                ? "{0} -i {1} -threads {2} -v warning -print_format json -show_streams -show_chapters -show_format"
                : "{0} -i {1} -threads {2} -v warning -print_format json -show_streams -show_format";

            if (protocol == MediaProtocol.File && !isAudio && _proberSupportsFirstVideoFrame)
            {
                args += " -show_frames -only_first_vframe";
            }

            args = string.Format(CultureInfo.InvariantCulture, args, probeSizeArgument, inputPath, _threads).Trim();

            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    CreateNoWindow = true,
                    UseShellExecute = false,

                    // Must consume both or ffmpeg may hang due to deadlocks.
                    RedirectStandardOutput = true,

                    FileName = _ffprobePath,
                    Arguments = args,

                    WindowStyle = ProcessWindowStyle.Hidden,
                    ErrorDialog = false,
                },
                EnableRaisingEvents = true
            };

            _logger.LogDebug("Starting {ProcessFileName} with args {ProcessArgs}", _ffprobePath, args);

            var memoryStream = new MemoryStream();
            await using (memoryStream.ConfigureAwait(false))
            using (var processWrapper = new ProcessWrapper(process, this))
            {
                StartProcess(processWrapper);
                using var reader = process.StandardOutput;
                await reader.BaseStream.CopyToAsync(memoryStream, cancellationToken).ConfigureAwait(false);
                memoryStream.Seek(0, SeekOrigin.Begin);
                InternalMediaInfoResult result;
                try
                {
                    result = await JsonSerializer.DeserializeAsync<InternalMediaInfoResult>(
                                        memoryStream,
                                        _jsonSerializerOptions,
                                        cancellationToken).ConfigureAwait(false);
                }
                catch
                {
                    StopProcess(processWrapper, 100);

                    throw;
                }

                if (result is null || (result.Streams is null && result.Format is null))
                {
                    throw new FfmpegException("ffprobe failed - streams and format are both null.");
                }

                if (result.Streams is not null)
                {
                    // Normalize aspect ratio if invalid
                    foreach (var stream in result.Streams)
                    {
                        if (string.Equals(stream.DisplayAspectRatio, "0:1", StringComparison.OrdinalIgnoreCase))
                        {
                            stream.DisplayAspectRatio = string.Empty;
                        }

                        if (string.Equals(stream.SampleAspectRatio, "0:1", StringComparison.OrdinalIgnoreCase))
                        {
                            stream.SampleAspectRatio = string.Empty;
                        }
                    }
                }

                return new ProbeResultNormalizer(_logger, _localization).GetMediaInfo(result, videoType, isAudio, primaryPath, protocol);
            }
        }

        /// <inheritdoc />
        public Task<string> ExtractAudioImage(string path, int? imageStreamIndex, CancellationToken cancellationToken)
        {
            var mediaSource = new MediaSourceInfo
            {
                Protocol = MediaProtocol.File
            };

            return ExtractImage(path, null, null, imageStreamIndex, mediaSource, true, null, null, ImageFormat.Jpg, cancellationToken);
        }

        /// <inheritdoc />
        public Task<string> ExtractVideoImage(string inputFile, string container, MediaSourceInfo mediaSource, MediaStream videoStream, Video3DFormat? threedFormat, TimeSpan? offset, CancellationToken cancellationToken)
        {
            return ExtractImage(inputFile, container, videoStream, null, mediaSource, false, threedFormat, offset, ImageFormat.Jpg, cancellationToken);
        }

        /// <inheritdoc />
        public Task<string> ExtractVideoImage(string inputFile, string container, MediaSourceInfo mediaSource, MediaStream imageStream, int? imageStreamIndex, ImageFormat? targetFormat, CancellationToken cancellationToken)
        {
            return ExtractImage(inputFile, container, imageStream, imageStreamIndex, mediaSource, false, null, null, targetFormat, cancellationToken);
        }

        private async Task<string> ExtractImage(
            string inputFile,
            string container,
            MediaStream videoStream,
            int? imageStreamIndex,
            MediaSourceInfo mediaSource,
            bool isAudio,
            Video3DFormat? threedFormat,
            TimeSpan? offset,
            ImageFormat? targetFormat,
            CancellationToken cancellationToken)
        {
            var inputArgument = GetInputPathArgument(inputFile, mediaSource);

            if (!isAudio)
            {
                try
                {
                    return await ExtractImageInternal(inputArgument, container, videoStream, imageStreamIndex, threedFormat, offset, true, targetFormat, false, cancellationToken).ConfigureAwait(false);
                }
                catch (ArgumentException)
                {
                    throw;
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(ex, "I-frame image extraction failed, will attempt standard way. Input: {Arguments}", inputArgument);
                }
            }

            return await ExtractImageInternal(inputArgument, container, videoStream, imageStreamIndex, threedFormat, offset, false, targetFormat, isAudio, cancellationToken).ConfigureAwait(false);
        }

        private string GetImageResolutionParameter()
        {
            var imageResolutionParameter = _serverConfig.Configuration.ChapterImageResolution switch
            {
                ImageResolution.P144 => "256x144",
                ImageResolution.P240 => "426x240",
                ImageResolution.P360 => "640x360",
                ImageResolution.P480 => "854x480",
                ImageResolution.P720 => "1280x720",
                ImageResolution.P1080 => "1920x1080",
                ImageResolution.P1440 => "2560x1440",
                ImageResolution.P2160 => "3840x2160",
                _ => string.Empty
            };

            if (!string.IsNullOrEmpty(imageResolutionParameter))
            {
                imageResolutionParameter = " -s " + imageResolutionParameter;
            }

            return imageResolutionParameter;
        }

        private async Task<string> ExtractImageInternal(
            string inputPath,
            string container,
            MediaStream videoStream,
            int? imageStreamIndex,
            Video3DFormat? threedFormat,
            TimeSpan? offset,
            bool useIFrame,
            ImageFormat? targetFormat,
            bool isAudio,
            CancellationToken cancellationToken)
        {
            ArgumentException.ThrowIfNullOrEmpty(inputPath);

            var useTradeoff = _config.GetFFmpegImgExtractPerfTradeoff();

            var outputExtension = targetFormat?.GetExtension() ?? ".jpg";

            var tempExtractPath = Path.Combine(_configurationManager.ApplicationPaths.TempDirectory, Guid.NewGuid() + outputExtension);
            Directory.CreateDirectory(Path.GetDirectoryName(tempExtractPath));

            // deint -> scale -> thumbnail -> tonemap.
            // put the SW tonemap right after the thumbnail to do it only once to reduce cpu usage.
            var filters = new List<string>();

            // deinterlace using bwdif algorithm for video stream.
            if (videoStream is not null && videoStream.IsInterlaced)
            {
                filters.Add("bwdif=0:-1:0");
            }

            // apply some filters to thumbnail extracted below (below) crop any black lines that we made and get the correct ar.
            // This filter chain may have adverse effects on recorded tv thumbnails if ar changes during presentation ex. commercials @ diff ar
            var scaler = threedFormat switch
            {
                // hsbs crop width in half,scale to correct size, set the display aspect,crop out any black bars we may have made. Work out the correct height based on the display aspect it will maintain the aspect where -1 in this case (3d) may not.
                Video3DFormat.HalfSideBySide => @"crop=iw/2:ih:0:0,scale=(iw*2):ih,setdar=dar=a,crop=min(iw\,ih*dar):min(ih\,iw/dar):(iw-min(iw\,iw*sar))/2:(ih - min (ih\,ih/sar))/2,setsar=sar=1",
                // fsbs crop width in half,set the display aspect,crop out any black bars we may have made
                Video3DFormat.FullSideBySide => @"crop=iw/2:ih:0:0,setdar=dar=a,crop=min(iw\,ih*dar):min(ih\,iw/dar):(iw-min(iw\,iw*sar))/2:(ih - min (ih\,ih/sar))/2,setsar=sar=1",
                // htab crop height in half,scale to correct size, set the display aspect,crop out any black bars we may have made
                Video3DFormat.HalfTopAndBottom => @"crop=iw:ih/2:0:0,scale=(iw*2):ih),setdar=dar=a,crop=min(iw\,ih*dar):min(ih\,iw/dar):(iw-min(iw\,iw*sar))/2:(ih - min (ih\,ih/sar))/2,setsar=sar=1",
                // ftab crop height in half, set the display aspect,crop out any black bars we may have made
                Video3DFormat.FullTopAndBottom => @"crop=iw:ih/2:0:0,setdar=dar=a,crop=min(iw\,ih*dar):min(ih\,iw/dar):(iw-min(iw\,iw*sar))/2:(ih - min (ih\,ih/sar))/2,setsar=sar=1",
                _ => "scale=round(iw*sar/2)*2:round(ih/2)*2"
            };

            filters.Add(scaler);

            // Use ffmpeg to sample N frames and pick the best thumbnail. Have a fall back just in case.
            var enableThumbnail = !useTradeoff && useIFrame && !string.Equals("wtv", container, StringComparison.OrdinalIgnoreCase);
            if (enableThumbnail)
            {
                filters.Add("thumbnail=n=24");
            }

            // Use SW tonemap on HDR video stream only when the zscale or tonemapx filter is available.
            // Only enable Dolby Vision tonemap when tonemapx is available
            var enableHdrExtraction = false;

            if (videoStream?.VideoRange == VideoRange.HDR)
            {
                if (SupportsFilter("tonemapx"))
                {
                    var peak = videoStream.VideoRangeType == VideoRangeType.DOVI ? "400" : "100";
                    enableHdrExtraction = true;
                    filters.Add($"tonemapx=tonemap=bt2390:desat=0:peak={peak}:t=bt709:m=bt709:p=bt709:format=yuv420p:range=full");
                }
                else if (SupportsFilter("zscale") && videoStream.VideoRangeType != VideoRangeType.DOVI)
                {
                    enableHdrExtraction = true;
                    filters.Add("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0:peak=100,zscale=t=bt709:m=bt709:out_range=full,format=yuv420p");
                }
            }

            var vf = string.Join(',', filters);
            var mapArg = imageStreamIndex.HasValue ? (" -map 0:" + imageStreamIndex.Value.ToString(CultureInfo.InvariantCulture)) : string.Empty;
            var args = string.Format(
                CultureInfo.InvariantCulture,
                "-i {0}{1} -threads {2} -v quiet -vframes 1 -vf {3}{4}{5} -f image2 \"{6}\"",
                inputPath,
                mapArg,
                _threads,
                vf,
                isAudio ? string.Empty : GetImageResolutionParameter(),
                EncodingHelper.GetVideoSyncOption("-1", EncoderVersion), // auto decide fps mode
                tempExtractPath);

            if (offset.HasValue)
            {
                args = string.Format(CultureInfo.InvariantCulture, "-ss {0} ", GetTimeParameter(offset.Value)) + args;
            }

            // The mpegts demuxer cannot seek to keyframes, so we have to let the
            // decoder discard non-keyframes, which may contain corrupted images.
            var seekMpegTs = offset.HasValue && string.Equals("mpegts", container, StringComparison.OrdinalIgnoreCase);
            if (useIFrame && (useTradeoff || seekMpegTs))
            {
                args = "-skip_frame nokey " + args;
            }

            if (!string.IsNullOrWhiteSpace(container))
            {
                var inputFormat = EncodingHelper.GetInputFormat(container);
                if (!string.IsNullOrWhiteSpace(inputFormat))
                {
                    args = "-f " + inputFormat + " " + args;
                }
            }

            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    FileName = _ffmpegPath,
                    Arguments = args,
                    WindowStyle = ProcessWindowStyle.Hidden,
                    ErrorDialog = false,
                },
                EnableRaisingEvents = true
            };

            _logger.LogDebug("{ProcessFileName} {ProcessArguments}", process.StartInfo.FileName, process.StartInfo.Arguments);

            using (var processWrapper = new ProcessWrapper(process, this))
            {
                using (await _thumbnailResourcePool.LockAsync(cancellationToken).ConfigureAwait(false))
                {
                    StartProcess(processWrapper);

                    var timeoutMs = _configurationManager.Configuration.ImageExtractionTimeoutMs;
                    if (timeoutMs <= 0)
                    {
                        timeoutMs = enableHdrExtraction ? DefaultHdrImageExtractionTimeout : DefaultSdrImageExtractionTimeout;
                    }

                    try
                    {
                        await process.WaitForExitAsync(TimeSpan.FromMilliseconds(timeoutMs)).ConfigureAwait(false);
                    }
                    catch (OperationCanceledException ex)
                    {
                        process.Kill(true);
                        throw new FfmpegException(string.Format(CultureInfo.InvariantCulture, "ffmpeg image extraction timed out for {0} after {1}ms", inputPath, timeoutMs), ex);
                    }
                }

                var file = _fileSystem.GetFileInfo(tempExtractPath);

                if (processWrapper.ExitCode > 0 || !file.Exists || file.Length == 0)
                {
                    throw new FfmpegException(string.Format(CultureInfo.InvariantCulture, "ffmpeg image extraction failed for {0}", inputPath));
                }

                return tempExtractPath;
            }
        }

        /// <inheritdoc />
        public async Task<string> ExtractVideoImagesOnIntervalAccelerated(
            string inputFile,
            string container,
            MediaSourceInfo mediaSource,
            MediaStream imageStream,
            int maxWidth,
            TimeSpan interval,
            bool allowHwAccel,
            bool enableHwEncoding,
            int? threads,
            int? qualityScale,
            ProcessPriorityClass? priority,
            bool enableKeyFrameOnlyExtraction,
            EncodingHelper encodingHelper,
            CancellationToken cancellationToken)
        {
            var options = allowHwAccel ? _configurationManager.GetEncodingOptions() : new EncodingOptions();
            threads ??= _threads;

            if (allowHwAccel && enableKeyFrameOnlyExtraction)
            {
                var hardwareAccelerationType = options.HardwareAccelerationType;
                var supportsKeyFrameOnly = (hardwareAccelerationType == HardwareAccelerationType.nvenc && options.EnableEnhancedNvdecDecoder)
                                           || (hardwareAccelerationType == HardwareAccelerationType.amf && OperatingSystem.IsWindows())
                                           || (hardwareAccelerationType == HardwareAccelerationType.qsv && options.PreferSystemNativeHwDecoder)
                                           || hardwareAccelerationType == HardwareAccelerationType.vaapi
                                           || hardwareAccelerationType == HardwareAccelerationType.videotoolbox
                                           || hardwareAccelerationType == HardwareAccelerationType.rkmpp;
                if (!supportsKeyFrameOnly)
                {
                    // Disable hardware acceleration when the hardware decoder does not support keyframe only mode.
                    allowHwAccel = false;
                    options = new EncodingOptions();
                }
            }

            // A new EncodingOptions instance must be used as to not disable HW acceleration for all of Jellyfin.
            // Additionally, we must set a few fields without defaults to prevent null pointer exceptions.
            if (!allowHwAccel)
            {
                options.EnableHardwareEncoding = false;
                options.HardwareAccelerationType = HardwareAccelerationType.none;
                options.EnableTonemapping = false;
            }

            if (imageStream.Width is not null && imageStream.Height is not null && !string.IsNullOrEmpty(imageStream.AspectRatio))
            {
                // For hardware trickplay encoders, we need to re-calculate the size because they used fixed scale dimensions
                var darParts = imageStream.AspectRatio.Split(':');
                var (wa, ha) = (double.Parse(darParts[0], CultureInfo.InvariantCulture), double.Parse(darParts[1], CultureInfo.InvariantCulture));
                // When dimension / DAR does not equal to 1:1, then the frames are most likely stored stretched.
                // Note: this might be incorrect for 3D videos as the SAR stored might be per eye instead of per video, but we really can do little about it.
                var shouldResetHeight = Math.Abs((imageStream.Width.Value * ha) - (imageStream.Height.Value * wa)) > .05;
                if (shouldResetHeight)
                {
                    // SAR = DAR * Height / Width
                    // RealHeight = Height / SAR = Height / (DAR * Height / Width) = Width / DAR
                    imageStream.Height = Convert.ToInt32(imageStream.Width.Value * ha / wa);
                }
            }

            var baseRequest = new BaseEncodingJobOptions { MaxWidth = maxWidth, MaxFramerate = (float)(1.0 / interval.TotalSeconds) };
            var jobState = new EncodingJobInfo(TranscodingJobType.Progressive)
            {
                IsVideoRequest = true,  // must be true for InputVideoHwaccelArgs to return non-empty value
                MediaSource = mediaSource,
                VideoStream = imageStream,
                BaseRequest = baseRequest,  // GetVideoProcessingFilterParam errors if null
                MediaPath = inputFile,
                OutputVideoCodec = "mjpeg"
            };
            var vidEncoder = enableHwEncoding ? encodingHelper.GetVideoEncoder(jobState, options) : jobState.OutputVideoCodec;

            // Get input and filter arguments
            var inputArg = encodingHelper.GetInputArgument(jobState, options, container).Trim();
            if (string.IsNullOrWhiteSpace(inputArg))
            {
                throw new InvalidOperationException("EncodingHelper returned empty input arguments.");
            }

            if (!allowHwAccel)
            {
                inputArg = "-threads " + threads + " " + inputArg; // HW accel args set a different input thread count, only set if disabled
            }

            if (options.HardwareAccelerationType == HardwareAccelerationType.videotoolbox && _isLowPriorityHwDecodeSupported)
            {
                // VideoToolbox supports low priority decoding, which is useful for trickplay
                inputArg = "-hwaccel_flags +low_priority " + inputArg;
            }

            var filterParam = encodingHelper.GetVideoProcessingFilterParam(jobState, options, vidEncoder).Trim();
            if (string.IsNullOrWhiteSpace(filterParam))
            {
                throw new InvalidOperationException("EncodingHelper returned empty or invalid filter parameters.");
            }

            try
            {
                return await ExtractVideoImagesOnIntervalInternal(
                    (enableKeyFrameOnlyExtraction ? "-skip_frame nokey " : string.Empty) + inputArg,
                    filterParam,
                    vidEncoder,
                    threads,
                    qualityScale,
                    priority,
                    cancellationToken).ConfigureAwait(false);
            }
            catch (FfmpegException ex)
            {
                if (!enableKeyFrameOnlyExtraction)
                {
                    throw;
                }

                _logger.LogWarning(ex, "I-frame trickplay extraction failed, will attempt standard way. Input: {InputFile}", inputFile);
            }

            return await ExtractVideoImagesOnIntervalInternal(inputArg, filterParam, vidEncoder, threads, qualityScale, priority, cancellationToken).ConfigureAwait(false);
        }

        private async Task<string> ExtractVideoImagesOnIntervalInternal(
            string inputArg,
            string filterParam,
            string vidEncoder,
            int? outputThreads,
            int? qualityScale,
            ProcessPriorityClass? priority,
            CancellationToken cancellationToken)
        {
            if (string.IsNullOrWhiteSpace(inputArg))
            {
                throw new InvalidOperationException("Empty or invalid input argument.");
            }

            // ffmpeg qscale is a value from 1-31, with 1 being best quality and 31 being worst
            // jpeg quality is a value from 0-100, with 0 being worst quality and 100 being best
            var encoderQuality = Math.Clamp(qualityScale ?? 4, 1, 31);
            var encoderQualityOption = "-qscale:v ";

            if (vidEncoder.Contains("vaapi", StringComparison.OrdinalIgnoreCase)
                || vidEncoder.Contains("qsv", StringComparison.OrdinalIgnoreCase))
            {
                // vaapi and qsv's mjpeg encoder use jpeg quality as input, instead of ffmpeg defined qscale
                encoderQuality = 100 - ((encoderQuality - 1) * (100 / 30));
                encoderQualityOption = "-global_quality:v ";
            }

            if (vidEncoder.Contains("videotoolbox", StringComparison.OrdinalIgnoreCase))
            {
                // videotoolbox's mjpeg encoder uses jpeg quality scaled to QP2LAMBDA (118) instead of ffmpeg defined qscale
                encoderQuality = 118 - ((encoderQuality - 1) * (118 / 30));
            }

            if (vidEncoder.Contains("rkmpp", StringComparison.OrdinalIgnoreCase))
            {
                // rkmpp's mjpeg encoder uses jpeg quality as input (max is 99, not 100), instead of ffmpeg defined qscale
                encoderQuality = 99 - ((encoderQuality - 1) * (99 / 30));
                encoderQualityOption = "-qp_init:v ";
            }

            // Output arguments
            var targetDirectory = Path.Combine(_configurationManager.ApplicationPaths.TempDirectory, Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(targetDirectory);
            var outputPath = Path.Combine(targetDirectory, "%08d.jpg");

            // Final command arguments
            var args = string.Format(
                CultureInfo.InvariantCulture,
                "-loglevel error {0} -an -sn {1} -threads {2} -c:v {3} {4}{5}{6}-f {7} \"{8}\"",
                inputArg,
                filterParam,
                outputThreads.GetValueOrDefault(_threads),
                vidEncoder,
                encoderQualityOption + encoderQuality + " ",
                vidEncoder.Contains("videotoolbox", StringComparison.InvariantCultureIgnoreCase) ? "-allow_sw 1 " : string.Empty, // allow_sw fallback for some intel macs
                EncodingHelper.GetVideoSyncOption("0", EncoderVersion).Trim() + " ", // passthrough timestamp
                "image2",
                outputPath);

            // Start ffmpeg process
            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    FileName = _ffmpegPath,
                    Arguments = args,
                    WindowStyle = ProcessWindowStyle.Hidden,
                    ErrorDialog = false,
                },
                EnableRaisingEvents = true
            };

            var processDescription = string.Format(CultureInfo.InvariantCulture, "{0} {1}", process.StartInfo.FileName, process.StartInfo.Arguments);
            _logger.LogInformation("Trickplay generation: {ProcessDescription}", processDescription);

            using (var processWrapper = new ProcessWrapper(process, this))
            {
                bool ranToCompletion = false;

                using (await _thumbnailResourcePool.LockAsync(cancellationToken).ConfigureAwait(false))
                {
                    StartProcess(processWrapper);

                    // Set process priority
                    if (priority.HasValue)
                    {
                        try
                        {
                            processWrapper.Process.PriorityClass = priority.Value;
                        }
                        catch (Exception ex)
                        {
                            _logger.LogDebug(ex, "Unable to set process priority to {Priority} for {Description}", priority.Value, processDescription);
                        }
                    }

                    // Need to give ffmpeg enough time to make all the thumbnails, which could be a while,
                    // but we still need to detect if the process hangs.
                    // Making the assumption that as long as new jpegs are showing up, everything is good.

                    bool isResponsive = true;
                    int lastCount = 0;
                    var timeoutMs = _configurationManager.Configuration.ImageExtractionTimeoutMs;
                    timeoutMs = timeoutMs <= 0 ? DefaultHdrImageExtractionTimeout : timeoutMs;

                    while (isResponsive && !cancellationToken.IsCancellationRequested)
                    {
                        try
                        {
                            await process.WaitForExitAsync(TimeSpan.FromMilliseconds(timeoutMs)).ConfigureAwait(false);

                            ranToCompletion = true;
                            break;
                        }
                        catch (OperationCanceledException)
                        {
                            // We don't actually expect the process to be finished in one timeout span, just that one image has been generated.
                        }

                        var jpegCount = _fileSystem.GetFilePaths(targetDirectory).Count();

                        isResponsive = jpegCount > lastCount;
                        lastCount = jpegCount;
                    }

                    if (!ranToCompletion)
                    {
                        if (!isResponsive)
                        {
                            _logger.LogInformation("Trickplay process unresponsive.");
                        }

                        _logger.LogInformation("Stopping trickplay extraction.");
                        StopProcess(processWrapper, 1000);
                    }
                }

                if (!ranToCompletion || processWrapper.ExitCode != 0)
                {
                    // Cleanup temp folder here, because the targetDirectory is not returned and the cleanup for failed ffmpeg process is not possible for caller.
                    // Ideally the ffmpeg should not write any files if it fails, but it seems like it is not guaranteed.
                    try
                    {
                        Directory.Delete(targetDirectory, true);
                    }
                    catch (Exception e)
                    {
                        _logger.LogError(e, "Failed to delete ffmpeg temp directory {TargetDirectory}", targetDirectory);
                    }

                    throw new FfmpegException(string.Format(CultureInfo.InvariantCulture, "ffmpeg image extraction failed for {0}", processDescription));
                }

                return targetDirectory;
            }
        }

        public string GetTimeParameter(long ticks)
        {
            var time = TimeSpan.FromTicks(ticks);

            return GetTimeParameter(time);
        }

        public string GetTimeParameter(TimeSpan time)
        {
            return time.ToString(@"hh\:mm\:ss\.fff", CultureInfo.InvariantCulture);
        }

        private void StartProcess(ProcessWrapper process)
        {
            process.Process.Start();

            try
            {
                process.Process.PriorityClass = ProcessPriorityClass.BelowNormal;
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Unable to set process priority to BelowNormal for {ProcessFileName}", process.Process.StartInfo.FileName);
            }

            lock (_runningProcessesLock)
            {
                _runningProcesses.Add(process);
            }
        }

        private void StopProcess(ProcessWrapper process, int waitTimeMs)
        {
            try
            {
                if (process.Process.WaitForExit(waitTimeMs))
                {
                    return;
                }

                _logger.LogInformation("Killing ffmpeg process");

                process.Process.Kill();
            }
            catch (InvalidOperationException)
            {
                // The process has already exited or
                // there is no process associated with this Process object.
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error killing process");
            }
        }

        private void StopProcesses()
        {
            List<ProcessWrapper> processes;
            lock (_runningProcessesLock)
            {
                processes = _runningProcesses.ToList();
                _runningProcesses.Clear();
            }

            foreach (var process in processes)
            {
                if (!process.HasExited)
                {
                    StopProcess(process, 500);
                }
            }
        }

        public string EscapeSubtitleFilterPath(string path)
        {
            // https://ffmpeg.org/ffmpeg-filters.html#Notes-on-filtergraph-escaping
            // We need to double escape

            return path
                .Replace('\\', '/')
                .Replace(":", "\\:", StringComparison.Ordinal)
                .Replace("'", @"'\\\''", StringComparison.Ordinal)
                .Replace("\"", "\\\"", StringComparison.Ordinal);
        }

        /// <inheritdoc />
        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        /// <summary>
        /// Releases unmanaged and - optionally - managed resources.
        /// </summary>
        /// <param name="dispose"><c>true</c> to release both managed and unmanaged resources; <c>false</c> to release only unmanaged resources.</param>
        protected virtual void Dispose(bool dispose)
        {
            if (dispose)
            {
                StopProcesses();
                _thumbnailResourcePool.Dispose();
            }
        }

        /// <inheritdoc />
        public Task ConvertImage(string inputPath, string outputPath)
        {
            throw new NotImplementedException();
        }

        /// <inheritdoc />
        public IReadOnlyList<string> GetPrimaryPlaylistVobFiles(string path, uint? titleNumber)
        {
            // Eliminate menus and intros by omitting VIDEO_TS.VOB and all subsequent title .vob files ending with _0.VOB
            var allVobs = _fileSystem.GetFiles(path, true)
                .Where(file => string.Equals(file.Extension, ".VOB", StringComparison.OrdinalIgnoreCase))
                .Where(file => !string.Equals(file.Name, "VIDEO_TS.VOB", StringComparison.OrdinalIgnoreCase))
                .Where(file => !file.Name.EndsWith("_0.VOB", StringComparison.OrdinalIgnoreCase))
                .OrderBy(i => i.FullName)
                .ToList();

            if (titleNumber.HasValue)
            {
                var prefix = string.Format(CultureInfo.InvariantCulture, "VTS_{0:D2}_", titleNumber.Value);
                var vobs = allVobs.Where(i => i.Name.StartsWith(prefix, StringComparison.OrdinalIgnoreCase)).ToList();

                if (vobs.Count > 0)
                {
                    return vobs.Select(i => i.FullName).ToList();
                }

                _logger.LogWarning("Could not determine .vob files for title {Title} of {Path}.", titleNumber, path);
            }

            // Check for multiple big titles (> 900 MB)
            var titles = allVobs
                .Where(vob => vob.Length >= 900 * 1024 * 1024)
                .Select(vob => _fileSystem.GetFileNameWithoutExtension(vob).AsSpan().RightPart('_').ToString())
                .Distinct()
                .ToList();

            // Fall back to first title if no big title is found
            if (titles.Count == 0)
            {
                titles.Add(_fileSystem.GetFileNameWithoutExtension(allVobs[0]).AsSpan().RightPart('_').ToString());
            }

            // Aggregate all .vob files of the titles
            return allVobs
                .Where(vob => titles.Contains(_fileSystem.GetFileNameWithoutExtension(vob).AsSpan().RightPart('_').ToString()))
                .Select(i => i.FullName)
                .Order()
                .ToList();
        }

        /// <inheritdoc />
        public IReadOnlyList<string> GetPrimaryPlaylistM2tsFiles(string path)
            => _blurayExaminer.GetDiscInfo(path).Files;

        /// <inheritdoc />
        public string GetInputPathArgument(EncodingJobInfo state)
            => GetInputPathArgument(state.MediaPath, state.MediaSource);

        /// <inheritdoc />
        public string GetInputPathArgument(string path, MediaSourceInfo mediaSource)
        {
            return mediaSource.VideoType switch
            {
                VideoType.Dvd => GetInputArgument(GetPrimaryPlaylistVobFiles(path, null), mediaSource),
                VideoType.BluRay => GetInputArgument(GetPrimaryPlaylistM2tsFiles(path), mediaSource),
                _ => GetInputArgument(path, mediaSource)
            };
        }

        /// <inheritdoc />
        public void GenerateConcatConfig(MediaSourceInfo source, string concatFilePath)
        {
            // Get all playable files
            IReadOnlyList<string> files;
            var videoType = source.VideoType;
            if (videoType == VideoType.Dvd)
            {
                files = GetPrimaryPlaylistVobFiles(source.Path, null);
            }
            else if (videoType == VideoType.BluRay)
            {
                files = GetPrimaryPlaylistM2tsFiles(source.Path);
            }
            else
            {
                return;
            }

            // Generate concat configuration entries for each file and write to file
            Directory.CreateDirectory(Path.GetDirectoryName(concatFilePath));
            using var sw = new FormattingStreamWriter(concatFilePath, CultureInfo.InvariantCulture);
            foreach (var path in files)
            {
                var mediaInfoResult = GetMediaInfo(
                    new MediaInfoRequest
                    {
                        MediaType = DlnaProfileType.Video,
                        MediaSource = new MediaSourceInfo
                        {
                            Path = path,
                            Protocol = MediaProtocol.File,
                            VideoType = videoType
                        }
                    },
                    CancellationToken.None).GetAwaiter().GetResult();

                var duration = TimeSpan.FromTicks(mediaInfoResult.RunTimeTicks.Value).TotalSeconds;

                // Add file path stanza to concat configuration
                sw.WriteLine("file '{0}'", path.Replace("'", @"'\''", StringComparison.Ordinal));

                // Add duration stanza to concat configuration
                sw.WriteLine("duration {0}", duration);
            }
        }

        public bool CanExtractSubtitles(string codec)
        {
            // TODO is there ever a case when a subtitle can't be extracted??
            return true;
        }

        private sealed class ProcessWrapper : IDisposable
        {
            private readonly MediaEncoder _mediaEncoder;

            private bool _disposed = false;

            public ProcessWrapper(Process process, MediaEncoder mediaEncoder)
            {
                Process = process;
                _mediaEncoder = mediaEncoder;
                Process.Exited += OnProcessExited;
            }

            public Process Process { get; }

            public bool HasExited { get; private set; }

            public int? ExitCode { get; private set; }

            private void OnProcessExited(object sender, EventArgs e)
            {
                var process = (Process)sender;

                HasExited = true;

                try
                {
                    ExitCode = process.ExitCode;
                }
                catch
                {
                }

                DisposeProcess(process);
            }

            private void DisposeProcess(Process process)
            {
                lock (_mediaEncoder._runningProcessesLock)
                {
                    _mediaEncoder._runningProcesses.Remove(this);
                }

                process.Dispose();
            }

            public void Dispose()
            {
                if (!_disposed)
                {
                    if (Process is not null)
                    {
                        Process.Exited -= OnProcessExited;
                        DisposeProcess(Process);
                    }
                }

                _disposed = true;
            }
        }
    }
}


# Encoder/ApplePlatformHelper.cs
#pragma warning disable CA1031

using System;
using System.Linq;
using System.Runtime.InteropServices;
using System.Runtime.Versioning;
using Microsoft.Extensions.Logging;

namespace MediaBrowser.MediaEncoding.Encoder;

/// <summary>
/// Helper class for Apple platform specific operations.
/// </summary>
[SupportedOSPlatform("macos")]
public static class ApplePlatformHelper
{
    private static readonly string[] _av1DecodeBlacklistedCpuClass = ["M1", "M2"];

    private static string GetSysctlValue(ReadOnlySpan<byte> name)
    {
        IntPtr length = IntPtr.Zero;
        // Get length of the value
        int osStatus = SysctlByName(name, IntPtr.Zero, ref length, IntPtr.Zero, 0);

        if (osStatus != 0)
        {
            throw new NotSupportedException($"Failed to get sysctl value for {System.Text.Encoding.UTF8.GetString(name)} with error {osStatus}");
        }

        IntPtr buffer = Marshal.AllocHGlobal(length.ToInt32());
        try
        {
            osStatus = SysctlByName(name, buffer, ref length, IntPtr.Zero, 0);
            if (osStatus != 0)
            {
                throw new NotSupportedException($"Failed to get sysctl value for {System.Text.Encoding.UTF8.GetString(name)} with error {osStatus}");
            }

            return Marshal.PtrToStringAnsi(buffer) ?? string.Empty;
        }
        finally
        {
            Marshal.FreeHGlobal(buffer);
        }
    }

    private static int SysctlByName(ReadOnlySpan<byte> name, IntPtr oldp, ref IntPtr oldlenp, IntPtr newp, uint newlen)
    {
        return NativeMethods.SysctlByName(name.ToArray(), oldp, ref oldlenp, newp, newlen);
    }

    /// <summary>
    /// Check if the current system has hardware acceleration for AV1 decoding.
    /// </summary>
    /// <param name="logger">The logger used for error logging.</param>
    /// <returns>Boolean indicates the hwaccel support.</returns>
    public static bool HasAv1HardwareAccel(ILogger logger)
    {
        if (!RuntimeInformation.OSArchitecture.Equals(Architecture.Arm64))
        {
            return false;
        }

        try
        {
            string cpuBrandString = GetSysctlValue("machdep.cpu.brand_string"u8);
            return !_av1DecodeBlacklistedCpuClass.Any(blacklistedCpuClass => cpuBrandString.Contains(blacklistedCpuClass, StringComparison.OrdinalIgnoreCase));
        }
        catch (NotSupportedException e)
        {
            logger.LogError("Error getting CPU brand string: {Message}", e.Message);
        }
        catch (Exception e)
        {
            logger.LogError("Unknown error occured: {Exception}", e);
        }

        return false;
    }

    private static class NativeMethods
    {
        [DllImport("libc", EntryPoint = "sysctlbyname", SetLastError = true)]
        [DefaultDllImportSearchPaths(DllImportSearchPath.SafeDirectories)]
        internal static extern int SysctlByName(byte[] name, IntPtr oldp, ref IntPtr oldlenp, IntPtr newp, uint newlen);
    }
}


# Encoder/EncodingUtils.cs
#pragma warning disable CS1591

using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using MediaBrowser.Model.MediaInfo;

namespace MediaBrowser.MediaEncoding.Encoder
{
    public static class EncodingUtils
    {
        public static string GetInputArgument(string inputPrefix, string inputFile, MediaProtocol protocol)
        {
            if (protocol != MediaProtocol.File)
            {
                return string.Format(CultureInfo.InvariantCulture, "\"{0}\"", inputFile);
            }

            return GetFileInputArgument(inputFile, inputPrefix);
        }

        public static string GetInputArgument(string inputPrefix, IReadOnlyList<string> inputFiles, MediaProtocol protocol)
        {
            if (protocol != MediaProtocol.File)
            {
                return string.Format(CultureInfo.InvariantCulture, "\"{0}\"", inputFiles[0]);
            }

            return GetConcatInputArgument(inputFiles, inputPrefix);
        }

        /// <summary>
        /// Gets the concat input argument.
        /// </summary>
        /// <param name="inputFiles">The input files.</param>
        /// <param name="inputPrefix">The input prefix.</param>
        /// <returns>System.String.</returns>
        private static string GetConcatInputArgument(IReadOnlyList<string> inputFiles, string inputPrefix)
        {
            // Get all streams
            // If there's more than one we'll need to use the concat command
            if (inputFiles.Count > 1)
            {
                var files = string.Join('|', inputFiles.Select(NormalizePath));

                return string.Format(CultureInfo.InvariantCulture, "concat:\"{0}\"", files);
            }

            // Determine the input path for video files
            return GetFileInputArgument(inputFiles[0], inputPrefix);
        }

        /// <summary>
        /// Gets the file input argument.
        /// </summary>
        /// <param name="path">The path.</param>
        /// <param name="inputPrefix">The path prefix.</param>
        /// <returns>System.String.</returns>
        private static string GetFileInputArgument(string path, string inputPrefix)
        {
            if (path.Contains("://", StringComparison.Ordinal))
            {
                return string.Format(CultureInfo.InvariantCulture, "\"{0}\"", path);
            }

            // Quotes are valid path characters in linux and they need to be escaped here with a leading \
            path = NormalizePath(path);

            return string.Format(CultureInfo.InvariantCulture, "{1}:\"{0}\"", path, inputPrefix);
        }

        /// <summary>
        /// Normalizes the path.
        /// </summary>
        /// <param name="path">The path.</param>
        /// <returns>System.String.</returns>
        public static string NormalizePath(string path)
        {
            // Quotes are valid path characters in linux and they need to be escaped here with a leading \
            return path.Replace("\"", "\\\"", StringComparison.Ordinal);
        }
    }
}


# Configuration/EncodingConfigurationStore.cs
#pragma warning disable CS1591

using System;
using System.Globalization;
using System.IO;
using MediaBrowser.Common.Configuration;
using MediaBrowser.Model.Configuration;

namespace MediaBrowser.MediaEncoding.Configuration
{
    public class EncodingConfigurationStore : ConfigurationStore, IValidatingConfiguration
    {
        public EncodingConfigurationStore()
        {
            ConfigurationType = typeof(EncodingOptions);
            Key = "encoding";
        }

        public void Validate(object oldConfig, object newConfig)
        {
            var oldEncodingOptions = (EncodingOptions)oldConfig;
            var newEncodingOptions = (EncodingOptions)newConfig;

            ArgumentNullException.ThrowIfNull(oldEncodingOptions, nameof(oldConfig));
            ArgumentNullException.ThrowIfNull(newEncodingOptions, nameof(newConfig));

            var newPath = newEncodingOptions.TranscodingTempPath;

            if (!string.IsNullOrWhiteSpace(newPath)
                && !string.Equals(oldEncodingOptions.TranscodingTempPath, newPath, StringComparison.Ordinal))
            {
                // Validate
                if (!Directory.Exists(newPath))
                {
                    throw new DirectoryNotFoundException(
                        string.Format(
                            CultureInfo.InvariantCulture,
                            "{0} does not exist.",
                            newPath));
                }
            }

            if (!string.IsNullOrWhiteSpace(newEncodingOptions.EncoderAppPath)
                && !string.Equals(oldEncodingOptions.EncoderAppPath, newEncodingOptions.EncoderAppPath, StringComparison.Ordinal))
            {
                throw new InvalidOperationException("Unable to update encoder app path.");
            }
        }
    }
}


# Configuration/EncodingConfigurationFactory.cs
#pragma warning disable CS1591

using System.Collections.Generic;
using MediaBrowser.Common.Configuration;

namespace MediaBrowser.MediaEncoding.Configuration
{
    public class EncodingConfigurationFactory : IConfigurationFactory
    {
        public IEnumerable<ConfigurationStore> GetConfigurations()
        {
            return new[]
            {
                new EncodingConfigurationStore()
            };
        }
    }
}


# Attachments/AttachmentExtractor.cs
using System;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using AsyncKeyedLock;
using MediaBrowser.Common.Extensions;
using MediaBrowser.Controller.Entities;
using MediaBrowser.Controller.IO;
using MediaBrowser.Controller.Library;
using MediaBrowser.Controller.MediaEncoding;
using MediaBrowser.MediaEncoding.Encoder;
using MediaBrowser.Model.Dto;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using Microsoft.Extensions.Logging;

namespace MediaBrowser.MediaEncoding.Attachments
{
    /// <inheritdoc cref="IAttachmentExtractor"/>
    public sealed class AttachmentExtractor : IAttachmentExtractor, IDisposable
    {
        private readonly ILogger<AttachmentExtractor> _logger;
        private readonly IFileSystem _fileSystem;
        private readonly IMediaEncoder _mediaEncoder;
        private readonly IMediaSourceManager _mediaSourceManager;
        private readonly IPathManager _pathManager;

        private readonly AsyncKeyedLocker<string> _semaphoreLocks = new(o =>
        {
            o.PoolSize = 20;
            o.PoolInitialFill = 1;
        });

        /// <summary>
        /// Initializes a new instance of the <see cref="AttachmentExtractor"/> class.
        /// </summary>
        /// <param name="logger">The <see cref="ILogger{AttachmentExtractor}"/>.</param>
        /// <param name="fileSystem">The <see cref="IFileSystem"/>.</param>
        /// <param name="mediaEncoder">The <see cref="IMediaEncoder"/>.</param>
        /// <param name="mediaSourceManager">The <see cref="IMediaSourceManager"/>.</param>
        /// <param name="pathManager">The <see cref="IPathManager"/>.</param>
        public AttachmentExtractor(
            ILogger<AttachmentExtractor> logger,
            IFileSystem fileSystem,
            IMediaEncoder mediaEncoder,
            IMediaSourceManager mediaSourceManager,
            IPathManager pathManager)
        {
            _logger = logger;
            _fileSystem = fileSystem;
            _mediaEncoder = mediaEncoder;
            _mediaSourceManager = mediaSourceManager;
            _pathManager = pathManager;
        }

        /// <inheritdoc />
        public async Task<(MediaAttachment Attachment, Stream Stream)> GetAttachment(BaseItem item, string mediaSourceId, int attachmentStreamIndex, CancellationToken cancellationToken)
        {
            ArgumentNullException.ThrowIfNull(item);

            if (string.IsNullOrWhiteSpace(mediaSourceId))
            {
                throw new ArgumentNullException(nameof(mediaSourceId));
            }

            var mediaSources = await _mediaSourceManager.GetPlaybackMediaSources(item, null, true, false, cancellationToken).ConfigureAwait(false);
            var mediaSource = mediaSources
                .FirstOrDefault(i => string.Equals(i.Id, mediaSourceId, StringComparison.OrdinalIgnoreCase));
            if (mediaSource is null)
            {
                throw new ResourceNotFoundException($"MediaSource {mediaSourceId} not found");
            }

            var mediaAttachment = mediaSource.MediaAttachments
                .FirstOrDefault(i => i.Index == attachmentStreamIndex);
            if (mediaAttachment is null)
            {
                throw new ResourceNotFoundException($"MediaSource {mediaSourceId} has no attachment with stream index {attachmentStreamIndex}");
            }

            if (string.Equals(mediaAttachment.Codec, "mjpeg", StringComparison.OrdinalIgnoreCase))
            {
                throw new ResourceNotFoundException($"Attachment with stream index {attachmentStreamIndex} can't be extracted for MediaSource {mediaSourceId}");
            }

            var attachmentStream = await GetAttachmentStream(mediaSource, mediaAttachment, cancellationToken)
                    .ConfigureAwait(false);

            return (mediaAttachment, attachmentStream);
        }

        /// <inheritdoc />
        public async Task ExtractAllAttachments(
            string inputFile,
            MediaSourceInfo mediaSource,
            CancellationToken cancellationToken)
        {
            var shouldExtractOneByOne = mediaSource.MediaAttachments.Any(a => !string.IsNullOrEmpty(a.FileName)
                                                                              && (a.FileName.Contains('/', StringComparison.OrdinalIgnoreCase) || a.FileName.Contains('\\', StringComparison.OrdinalIgnoreCase)));
            if (shouldExtractOneByOne && !inputFile.EndsWith(".mks", StringComparison.OrdinalIgnoreCase))
            {
                foreach (var attachment in mediaSource.MediaAttachments)
                {
                    if (!string.Equals(attachment.Codec, "mjpeg", StringComparison.OrdinalIgnoreCase))
                    {
                        await ExtractAttachment(inputFile, mediaSource, attachment, cancellationToken).ConfigureAwait(false);
                    }
                }
            }
            else
            {
                await ExtractAllAttachmentsInternal(
                    inputFile,
                    mediaSource,
                    false,
                    cancellationToken).ConfigureAwait(false);
            }
        }

        private async Task ExtractAllAttachmentsInternal(
            string inputFile,
            MediaSourceInfo mediaSource,
            bool isExternal,
            CancellationToken cancellationToken)
        {
            var inputPath = _mediaEncoder.GetInputArgument(inputFile, mediaSource);

            ArgumentException.ThrowIfNullOrEmpty(inputPath);

            var outputFolder = _pathManager.GetAttachmentFolderPath(mediaSource.Id);
            using (await _semaphoreLocks.LockAsync(outputFolder, cancellationToken).ConfigureAwait(false))
            {
                var directory = Directory.CreateDirectory(outputFolder);
                var fileNames = directory.GetFiles("*", SearchOption.TopDirectoryOnly).Select(f => f.Name).ToHashSet();
                var missingFiles = mediaSource.MediaAttachments.Where(a => a.FileName is not null && !fileNames.Contains(a.FileName) && !string.Equals(a.Codec, "mjpeg", StringComparison.OrdinalIgnoreCase));
                if (!missingFiles.Any())
                {
                    // Skip extraction if all files already exist
                    return;
                }

                var processArgs = string.Format(
                    CultureInfo.InvariantCulture,
                    "-dump_attachment:t \"\" -y {0} -i {1} -t 0 -f null null",
                    inputPath.EndsWith(".concat\"", StringComparison.OrdinalIgnoreCase) ? "-f concat -safe 0" : string.Empty,
                    inputPath);

                int exitCode;

                using (var process = new Process
                    {
                        StartInfo = new ProcessStartInfo
                        {
                            Arguments = processArgs,
                            FileName = _mediaEncoder.EncoderPath,
                            UseShellExecute = false,
                            CreateNoWindow = true,
                            WindowStyle = ProcessWindowStyle.Hidden,
                            WorkingDirectory = outputFolder,
                            ErrorDialog = false
                        },
                        EnableRaisingEvents = true
                    })
                {
                    _logger.LogInformation("{File} {Arguments}", process.StartInfo.FileName, process.StartInfo.Arguments);

                    process.Start();

                    try
                    {
                        await process.WaitForExitAsync(cancellationToken).ConfigureAwait(false);
                        exitCode = process.ExitCode;
                    }
                    catch (OperationCanceledException)
                    {
                        process.Kill(true);
                        exitCode = -1;
                    }
                }

                var failed = false;

                if (exitCode != 0)
                {
                    if (isExternal && exitCode == 1)
                    {
                        // ffmpeg returns exitCode 1 because there is no video or audio stream
                        // this can be ignored
                    }
                    else
                    {
                        failed = true;

                        _logger.LogWarning("Deleting extracted attachments {Path} due to failure: {ExitCode}", outputFolder, exitCode);
                        try
                        {
                            Directory.Delete(outputFolder);
                        }
                        catch (IOException ex)
                        {
                            _logger.LogError(ex, "Error deleting extracted attachments {Path}", outputFolder);
                        }
                    }
                }
                else if (!Directory.Exists(outputFolder))
                {
                    failed = true;
                }

                if (failed)
                {
                    _logger.LogError("ffmpeg attachment extraction failed for {InputPath} to {OutputPath}", inputPath, outputFolder);

                    throw new InvalidOperationException(
                        string.Format(CultureInfo.InvariantCulture, "ffmpeg attachment extraction failed for {0} to {1}", inputPath, outputFolder));
                }

                _logger.LogInformation("ffmpeg attachment extraction completed for {InputPath} to {OutputPath}", inputPath, outputFolder);
            }
        }

        private async Task<Stream> GetAttachmentStream(
            MediaSourceInfo mediaSource,
            MediaAttachment mediaAttachment,
            CancellationToken cancellationToken)
        {
            var attachmentPath = await ExtractAttachment(mediaSource.Path, mediaSource, mediaAttachment, cancellationToken)
                .ConfigureAwait(false);
            return AsyncFile.OpenRead(attachmentPath);
        }

        private async Task<string> ExtractAttachment(
            string inputFile,
            MediaSourceInfo mediaSource,
            MediaAttachment mediaAttachment,
            CancellationToken cancellationToken)
        {
            var attachmentFolderPath = _pathManager.GetAttachmentFolderPath(mediaSource.Id);
            using (await _semaphoreLocks.LockAsync(attachmentFolderPath, cancellationToken).ConfigureAwait(false))
            {
                var attachmentPath = _pathManager.GetAttachmentPath(mediaSource.Id, mediaAttachment.FileName ?? mediaAttachment.Index.ToString(CultureInfo.InvariantCulture));
                if (!File.Exists(attachmentPath))
                {
                    await ExtractAttachmentInternal(
                        _mediaEncoder.GetInputArgument(inputFile, mediaSource),
                        mediaAttachment.Index,
                        attachmentPath,
                        cancellationToken).ConfigureAwait(false);
                }

                return attachmentPath;
            }
        }

        private async Task ExtractAttachmentInternal(
            string inputPath,
            int attachmentStreamIndex,
            string outputPath,
            CancellationToken cancellationToken)
        {
            ArgumentException.ThrowIfNullOrEmpty(inputPath);

            ArgumentException.ThrowIfNullOrEmpty(outputPath);

            Directory.CreateDirectory(Path.GetDirectoryName(outputPath) ?? throw new ArgumentException("Path can't be a root directory.", nameof(outputPath)));

            var processArgs = string.Format(
                CultureInfo.InvariantCulture,
                "-dump_attachment:{1} \"{2}\" -i {0} -t 0 -f null null",
                inputPath,
                attachmentStreamIndex,
                EncodingUtils.NormalizePath(outputPath));

            int exitCode;

            using (var process = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        Arguments = processArgs,
                        FileName = _mediaEncoder.EncoderPath,
                        UseShellExecute = false,
                        CreateNoWindow = true,
                        WindowStyle = ProcessWindowStyle.Hidden,
                        ErrorDialog = false
                    },
                    EnableRaisingEvents = true
                })
            {
                _logger.LogInformation("{File} {Arguments}", process.StartInfo.FileName, process.StartInfo.Arguments);

                process.Start();

                try
                {
                    await process.WaitForExitAsync(cancellationToken).ConfigureAwait(false);
                    exitCode = process.ExitCode;
                }
                catch (OperationCanceledException)
                {
                    process.Kill(true);
                    exitCode = -1;
                }
            }

            var failed = false;

            if (exitCode != 0)
            {
                failed = true;

                _logger.LogWarning("Deleting extracted attachment {Path} due to failure: {ExitCode}", outputPath, exitCode);
                try
                {
                    if (File.Exists(outputPath))
                    {
                        _fileSystem.DeleteFile(outputPath);
                    }
                }
                catch (IOException ex)
                {
                    _logger.LogError(ex, "Error deleting extracted attachment {Path}", outputPath);
                }
            }
            else if (!File.Exists(outputPath))
            {
                failed = true;
            }

            if (failed)
            {
                _logger.LogError("ffmpeg attachment extraction failed for {InputPath} to {OutputPath}", inputPath, outputPath);

                throw new InvalidOperationException(
                    string.Format(CultureInfo.InvariantCulture, "ffmpeg attachment extraction failed for {0} to {1}", inputPath, outputPath));
            }

            _logger.LogInformation("ffmpeg attachment extraction completed for {InputPath} to {OutputPath}", inputPath, outputPath);
        }

        /// <inheritdoc />
        public void Dispose()
        {
            _semaphoreLocks.Dispose();
        }
    }
}


# Subtitles/ISubtitleParser.cs
#pragma warning disable CS1591

using System.IO;
using MediaBrowser.Model.MediaInfo;

namespace MediaBrowser.MediaEncoding.Subtitles
{
    public interface ISubtitleParser
    {
        /// <summary>
        /// Parses the specified stream.
        /// </summary>
        /// <param name="stream">The stream.</param>
        /// <param name="fileExtension">The file extension.</param>
        /// <returns>SubtitleTrackInfo.</returns>
        SubtitleTrackInfo Parse(Stream stream, string fileExtension);

        /// <summary>
        /// Determines whether the file extension is supported by the parser.
        /// </summary>
        /// <param name="fileExtension">The file extension.</param>
        /// <returns>A value indicating whether the file extension is supported.</returns>
        bool SupportsFileExtension(string fileExtension);
    }
}


# Subtitles/SsaWriter.cs
using System;
using System.Globalization;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using MediaBrowser.Model.MediaInfo;

namespace MediaBrowser.MediaEncoding.Subtitles
{
    /// <summary>
    /// SSA subtitle writer.
    /// </summary>
    public partial class SsaWriter : ISubtitleWriter
    {
        [GeneratedRegex(@"\n", RegexOptions.IgnoreCase)]
        private static partial Regex NewLineRegex();

        /// <inheritdoc />
        public void Write(SubtitleTrackInfo info, Stream stream, CancellationToken cancellationToken)
        {
            using (var writer = new StreamWriter(stream, Encoding.UTF8, 1024, true))
            {
                var trackEvents = info.TrackEvents;
                var timeFormat = @"hh\:mm\:ss\.ff";

                // Write SSA header
                writer.WriteLine("[Script Info]");
                writer.WriteLine("Title: Jellyfin transcoded SSA subtitle");
                writer.WriteLine("ScriptType: v4.00");
                writer.WriteLine();
                writer.WriteLine("[V4 Styles]");
                writer.WriteLine("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding");
                writer.WriteLine("Style: Default,Arial,20,&H00FFFFFF,&H00FFFFFF,&H19333333,&H19333333,0,0,0,1,0,2,10,10,10,0,1");
                writer.WriteLine();
                writer.WriteLine("[Events]");
                writer.WriteLine("Format: Layer, Start, End, Style, Text");

                for (int i = 0; i < trackEvents.Count; i++)
                {
                    cancellationToken.ThrowIfCancellationRequested();

                    var trackEvent = trackEvents[i];
                    var startTime = TimeSpan.FromTicks(trackEvent.StartPositionTicks).ToString(timeFormat, CultureInfo.InvariantCulture);
                    var endTime = TimeSpan.FromTicks(trackEvent.EndPositionTicks).ToString(timeFormat, CultureInfo.InvariantCulture);
                    var text = NewLineRegex().Replace(trackEvent.Text, "\\n");

                    writer.WriteLine(
                        "Dialogue: 0,{0},{1},Default,{2}",
                        startTime,
                        endTime,
                        text);
                }
            }
        }
    }
}


# Subtitles/VttWriter.cs
using System;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using MediaBrowser.Model.MediaInfo;

namespace MediaBrowser.MediaEncoding.Subtitles
{
    /// <summary>
    /// Subtitle writer for the WebVTT format.
    /// </summary>
    public partial class VttWriter : ISubtitleWriter
    {
        [GeneratedRegex(@"\\n", RegexOptions.IgnoreCase)]
        private static partial Regex NewlineEscapeRegex();

        /// <inheritdoc />
        public void Write(SubtitleTrackInfo info, Stream stream, CancellationToken cancellationToken)
        {
            using (var writer = new StreamWriter(stream, Encoding.UTF8, 1024, true))
            {
                writer.WriteLine("WEBVTT");
                writer.WriteLine();
                writer.WriteLine("Region: id:subtitle width:80% lines:3 regionanchor:50%,100% viewportanchor:50%,90%");
                writer.WriteLine();
                foreach (var trackEvent in info.TrackEvents)
                {
                    cancellationToken.ThrowIfCancellationRequested();

                    var startTime = TimeSpan.FromTicks(trackEvent.StartPositionTicks);
                    var endTime = TimeSpan.FromTicks(trackEvent.EndPositionTicks);

                    // make sure the start and end times are different and sequential
                    if (endTime.TotalMilliseconds <= startTime.TotalMilliseconds)
                    {
                        endTime = startTime.Add(TimeSpan.FromMilliseconds(1));
                    }

                    writer.WriteLine(@"{0:hh\:mm\:ss\.fff} --> {1:hh\:mm\:ss\.fff} region:subtitle line:90%", startTime, endTime);

                    var text = trackEvent.Text;

                    // TODO: Not sure how to handle these
                    text = NewlineEscapeRegex().Replace(text, " ");

                    writer.WriteLine(text);
                    writer.WriteLine();
                }
            }
        }
    }
}


# Subtitles/JsonWriter.cs
using System.IO;
using System.Text.Json;
using System.Threading;
using MediaBrowser.Model.MediaInfo;

namespace MediaBrowser.MediaEncoding.Subtitles
{
    /// <summary>
    /// JSON subtitle writer.
    /// </summary>
    public class JsonWriter : ISubtitleWriter
    {
        /// <inheritdoc />
        public void Write(SubtitleTrackInfo info, Stream stream, CancellationToken cancellationToken)
        {
            using (var writer = new Utf8JsonWriter(stream))
            {
                var trackevents = info.TrackEvents;
                writer.WriteStartObject();
                writer.WriteStartArray("TrackEvents");

                for (int i = 0; i < trackevents.Count; i++)
                {
                    cancellationToken.ThrowIfCancellationRequested();

                    var current = trackevents[i];
                    writer.WriteStartObject();

                    writer.WriteString("Id", current.Id);
                    writer.WriteString("Text", current.Text);
                    writer.WriteNumber("StartPositionTicks", current.StartPositionTicks);
                    writer.WriteNumber("EndPositionTicks", current.EndPositionTicks);

                    writer.WriteEndObject();
                }

                writer.WriteEndArray();
                writer.WriteEndObject();

                writer.Flush();
            }
        }
    }
}


# Subtitles/SubtitleFormatExtensions.cs
using System.Diagnostics.CodeAnalysis;
using Nikse.SubtitleEdit.Core.SubtitleFormats;

namespace MediaBrowser.MediaEncoding.Subtitles;

internal static class SubtitleFormatExtensions
{
    /// <summary>
    /// Will try to find errors if supported by provider.
    /// </summary>
    /// <param name="format">The subtitle format.</param>
    /// <param name="errors">The out errors value.</param>
    /// <returns>True if errors are available for given format.</returns>
    public static bool TryGetErrors(this SubtitleFormat format, [NotNullWhen(true)] out string? errors)
    {
        errors = format switch
        {
            SubStationAlpha ssa => ssa.Errors,
            AdvancedSubStationAlpha assa => assa.Errors,
            SubRip subRip => subRip.Errors,
            MicroDvd microDvd => microDvd.Errors,
            DCinemaSmpte2007 smpte2007 => smpte2007.Errors,
            DCinemaSmpte2010 smpte2010 => smpte2010.Errors,
            _ => null,
        };

        return !string.IsNullOrWhiteSpace(errors);
    }
}


# Subtitles/TtmlWriter.cs
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using MediaBrowser.Model.MediaInfo;

namespace MediaBrowser.MediaEncoding.Subtitles
{
    /// <summary>
    /// TTML subtitle writer.
    /// </summary>
    public partial class TtmlWriter : ISubtitleWriter
    {
        [GeneratedRegex(@"\\n", RegexOptions.IgnoreCase)]
        private static partial Regex NewLineEscapeRegex();

        /// <inheritdoc />
        public void Write(SubtitleTrackInfo info, Stream stream, CancellationToken cancellationToken)
        {
            // Example: https://github.com/zmalltalker/ttml2vtt/blob/master/data/sample.xml
            // Parser example: https://github.com/mozilla/popcorn-js/blob/master/parsers/parserTTML/popcorn.parserTTML.js

            using (var writer = new StreamWriter(stream, Encoding.UTF8, 1024, true))
            {
                writer.WriteLine("<?xml version=\"1.0\" encoding=\"utf-8\"?>");
                writer.WriteLine("<tt xmlns=\"http://www.w3.org/ns/ttml\" xmlns:tts=\"http://www.w3.org/2006/04/ttaf1#styling\" lang=\"no\">");

                writer.WriteLine("<head>");
                writer.WriteLine("<styling>");
                writer.WriteLine("<style id=\"italic\" tts:fontStyle=\"italic\" />");
                writer.WriteLine("<style id=\"left\" tts:textAlign=\"left\" />");
                writer.WriteLine("<style id=\"center\" tts:textAlign=\"center\" />");
                writer.WriteLine("<style id=\"right\" tts:textAlign=\"right\" />");
                writer.WriteLine("</styling>");
                writer.WriteLine("</head>");

                writer.WriteLine("<body>");
                writer.WriteLine("<div>");

                foreach (var trackEvent in info.TrackEvents)
                {
                    var text = trackEvent.Text;

                    text = NewLineEscapeRegex().Replace(text, "<br/>");

                    writer.WriteLine(
                        "<p begin=\"{0}\" dur=\"{1}\">{2}</p>",
                        trackEvent.StartPositionTicks,
                        trackEvent.EndPositionTicks - trackEvent.StartPositionTicks,
                        text);
                }

                writer.WriteLine("</div>");
                writer.WriteLine("</body>");

                writer.WriteLine("</tt>");
            }
        }
    }
}


# Subtitles/SubtitleEncoder.cs
#pragma warning disable CS1591

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Diagnostics.CodeAnalysis;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using AsyncKeyedLock;
using MediaBrowser.Common;
using MediaBrowser.Common.Configuration;
using MediaBrowser.Common.Extensions;
using MediaBrowser.Common.Net;
using MediaBrowser.Controller.Configuration;
using MediaBrowser.Controller.Entities;
using MediaBrowser.Controller.IO;
using MediaBrowser.Controller.Library;
using MediaBrowser.Controller.MediaEncoding;
using MediaBrowser.Model.Dto;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.MediaInfo;
using Microsoft.Extensions.Logging;
using UtfUnknown;

namespace MediaBrowser.MediaEncoding.Subtitles
{
    public sealed class SubtitleEncoder : ISubtitleEncoder, IDisposable
    {
        private readonly ILogger<SubtitleEncoder> _logger;
        private readonly IFileSystem _fileSystem;
        private readonly IMediaEncoder _mediaEncoder;
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly IMediaSourceManager _mediaSourceManager;
        private readonly ISubtitleParser _subtitleParser;
        private readonly IPathManager _pathManager;
        private readonly IServerConfigurationManager _serverConfigurationManager;

        /// <summary>
        /// The _semaphoreLocks.
        /// </summary>
        private readonly AsyncKeyedLocker<string> _semaphoreLocks = new(o =>
        {
            o.PoolSize = 20;
            o.PoolInitialFill = 1;
        });

        public SubtitleEncoder(
            ILogger<SubtitleEncoder> logger,
            IFileSystem fileSystem,
            IMediaEncoder mediaEncoder,
            IHttpClientFactory httpClientFactory,
            IMediaSourceManager mediaSourceManager,
            ISubtitleParser subtitleParser,
            IPathManager pathManager,
            IServerConfigurationManager serverConfigurationManager)
        {
            _logger = logger;
            _fileSystem = fileSystem;
            _mediaEncoder = mediaEncoder;
            _httpClientFactory = httpClientFactory;
            _mediaSourceManager = mediaSourceManager;
            _subtitleParser = subtitleParser;
            _pathManager = pathManager;
            _serverConfigurationManager = serverConfigurationManager;
        }

        private MemoryStream ConvertSubtitles(
            Stream stream,
            string inputFormat,
            string outputFormat,
            long startTimeTicks,
            long endTimeTicks,
            bool preserveOriginalTimestamps,
            CancellationToken cancellationToken)
        {
            var ms = new MemoryStream();

            try
            {
                var trackInfo = _subtitleParser.Parse(stream, inputFormat);

                FilterEvents(trackInfo, startTimeTicks, endTimeTicks, preserveOriginalTimestamps);

                var writer = GetWriter(outputFormat);

                writer.Write(trackInfo, ms, cancellationToken);
                ms.Position = 0;
            }
            catch
            {
                ms.Dispose();
                throw;
            }

            return ms;
        }

        private void FilterEvents(SubtitleTrackInfo track, long startPositionTicks, long endTimeTicks, bool preserveTimestamps)
        {
            // Drop subs that are earlier than what we're looking for
            track.TrackEvents = track.TrackEvents
                .SkipWhile(i => (i.StartPositionTicks - startPositionTicks) < 0 || (i.EndPositionTicks - startPositionTicks) < 0)
                .ToArray();

            if (endTimeTicks > 0)
            {
                track.TrackEvents = track.TrackEvents
                    .TakeWhile(i => i.StartPositionTicks <= endTimeTicks)
                    .ToArray();
            }

            if (!preserveTimestamps)
            {
                foreach (var trackEvent in track.TrackEvents)
                {
                    trackEvent.EndPositionTicks -= startPositionTicks;
                    trackEvent.StartPositionTicks -= startPositionTicks;
                }
            }
        }

        async Task<Stream> ISubtitleEncoder.GetSubtitles(BaseItem item, string mediaSourceId, int subtitleStreamIndex, string outputFormat, long startTimeTicks, long endTimeTicks, bool preserveOriginalTimestamps, CancellationToken cancellationToken)
        {
            ArgumentNullException.ThrowIfNull(item);

            if (string.IsNullOrWhiteSpace(mediaSourceId))
            {
                throw new ArgumentNullException(nameof(mediaSourceId));
            }

            var mediaSources = await _mediaSourceManager.GetPlaybackMediaSources(item, null, true, false, cancellationToken).ConfigureAwait(false);

            var mediaSource = mediaSources
                .First(i => string.Equals(i.Id, mediaSourceId, StringComparison.OrdinalIgnoreCase));

            var subtitleStream = mediaSource.MediaStreams
               .First(i => i.Type == MediaStreamType.Subtitle && i.Index == subtitleStreamIndex);

            var (stream, inputFormat) = await GetSubtitleStream(mediaSource, subtitleStream, cancellationToken)
                        .ConfigureAwait(false);

            // Return the original if the same format is being requested
            // Character encoding was already handled in GetSubtitleStream
            if (string.Equals(inputFormat, outputFormat, StringComparison.OrdinalIgnoreCase))
            {
                return stream;
            }

            using (stream)
            {
                return ConvertSubtitles(stream, inputFormat, outputFormat, startTimeTicks, endTimeTicks, preserveOriginalTimestamps, cancellationToken);
            }
        }

        private async Task<(Stream Stream, string Format)> GetSubtitleStream(
            MediaSourceInfo mediaSource,
            MediaStream subtitleStream,
            CancellationToken cancellationToken)
        {
            var fileInfo = await GetReadableFile(mediaSource, subtitleStream, cancellationToken).ConfigureAwait(false);

            var stream = await GetSubtitleStream(fileInfo, cancellationToken).ConfigureAwait(false);

            return (stream, fileInfo.Format);
        }

        private async Task<Stream> GetSubtitleStream(SubtitleInfo fileInfo, CancellationToken cancellationToken)
        {
            if (fileInfo.IsExternal)
            {
                var stream = await GetStream(fileInfo.Path, fileInfo.Protocol, cancellationToken).ConfigureAwait(false);
                await using (stream.ConfigureAwait(false))
                {
                    var result = await CharsetDetector.DetectFromStreamAsync(stream, cancellationToken).ConfigureAwait(false);
                    var detected = result.Detected;
                    stream.Position = 0;

                    if (detected is not null)
                    {
                        _logger.LogDebug("charset {CharSet} detected for {Path}", detected.EncodingName, fileInfo.Path);

                        using var reader = new StreamReader(stream, detected.Encoding);
                        var text = await reader.ReadToEndAsync(cancellationToken).ConfigureAwait(false);

                        return new MemoryStream(Encoding.UTF8.GetBytes(text));
                    }
                }
            }

            return AsyncFile.OpenRead(fileInfo.Path);
        }

        internal async Task<SubtitleInfo> GetReadableFile(
            MediaSourceInfo mediaSource,
            MediaStream subtitleStream,
            CancellationToken cancellationToken)
        {
            if (!subtitleStream.IsExternal || subtitleStream.Path.EndsWith(".mks", StringComparison.OrdinalIgnoreCase))
            {
                await ExtractAllExtractableSubtitles(mediaSource, cancellationToken).ConfigureAwait(false);

                var outputFileExtension = GetExtractableSubtitleFileExtension(subtitleStream);
                var outputFormat = GetExtractableSubtitleFormat(subtitleStream);
                var outputPath = GetSubtitleCachePath(mediaSource, subtitleStream.Index, "." + outputFileExtension);

                return new SubtitleInfo()
                {
                    Path = outputPath,
                    Protocol = MediaProtocol.File,
                    Format = outputFormat,
                    IsExternal = false
                };
            }

            var currentFormat = (Path.GetExtension(subtitleStream.Path) ?? subtitleStream.Codec)
                .TrimStart('.');

            // Handle PGS subtitles as raw streams for the client to render
            if (MediaStream.IsPgsFormat(currentFormat))
            {
                return new SubtitleInfo()
                {
                    Path = subtitleStream.Path,
                    Protocol = _mediaSourceManager.GetPathProtocol(subtitleStream.Path),
                    Format = "pgssub",
                    IsExternal = true
                };
            }

            // Fallback to ffmpeg conversion
            if (!_subtitleParser.SupportsFileExtension(currentFormat))
            {
                // Convert
                var outputPath = GetSubtitleCachePath(mediaSource, subtitleStream.Index, ".srt");

                await ConvertTextSubtitleToSrt(subtitleStream, mediaSource, outputPath, cancellationToken).ConfigureAwait(false);

                return new SubtitleInfo()
                {
                    Path = outputPath,
                    Protocol = MediaProtocol.File,
                    Format = "srt",
                    IsExternal = true
                };
            }

            // It's possible that the subtitleStream and mediaSource don't share the same protocol (e.g. .STRM file with local subs)
            return new SubtitleInfo()
            {
                Path = subtitleStream.Path,
                Protocol = _mediaSourceManager.GetPathProtocol(subtitleStream.Path),
                Format = currentFormat,
                IsExternal = true
            };
        }

        private bool TryGetWriter(string format, [NotNullWhen(true)] out ISubtitleWriter? value)
        {
            ArgumentException.ThrowIfNullOrEmpty(format);

            if (string.Equals(format, SubtitleFormat.ASS, StringComparison.OrdinalIgnoreCase))
            {
                value = new AssWriter();
                return true;
            }

            if (string.Equals(format, "json", StringComparison.OrdinalIgnoreCase))
            {
                value = new JsonWriter();
                return true;
            }

            if (string.Equals(format, SubtitleFormat.SRT, StringComparison.OrdinalIgnoreCase) || string.Equals(format, SubtitleFormat.SUBRIP, StringComparison.OrdinalIgnoreCase))
            {
                value = new SrtWriter();
                return true;
            }

            if (string.Equals(format, SubtitleFormat.SSA, StringComparison.OrdinalIgnoreCase))
            {
                value = new SsaWriter();
                return true;
            }

            if (string.Equals(format, SubtitleFormat.VTT, StringComparison.OrdinalIgnoreCase) || string.Equals(format, SubtitleFormat.WEBVTT, StringComparison.OrdinalIgnoreCase))
            {
                value = new VttWriter();
                return true;
            }

            if (string.Equals(format, SubtitleFormat.TTML, StringComparison.OrdinalIgnoreCase))
            {
                value = new TtmlWriter();
                return true;
            }

            value = null;
            return false;
        }

        private ISubtitleWriter GetWriter(string format)
        {
            if (TryGetWriter(format, out var writer))
            {
                return writer;
            }

            throw new ArgumentException("Unsupported format: " + format);
        }

        /// <summary>
        /// Converts the text subtitle to SRT.
        /// </summary>
        /// <param name="subtitleStream">The subtitle stream.</param>
        /// <param name="mediaSource">The input mediaSource.</param>
        /// <param name="outputPath">The output path.</param>
        /// <param name="cancellationToken">The cancellation token.</param>
        /// <returns>Task.</returns>
        private async Task ConvertTextSubtitleToSrt(MediaStream subtitleStream, MediaSourceInfo mediaSource, string outputPath, CancellationToken cancellationToken)
        {
            using (await _semaphoreLocks.LockAsync(outputPath, cancellationToken).ConfigureAwait(false))
            {
                if (!File.Exists(outputPath))
                {
                    await ConvertTextSubtitleToSrtInternal(subtitleStream, mediaSource, outputPath, cancellationToken).ConfigureAwait(false);
                }
            }
        }

        /// <summary>
        /// Converts the text subtitle to SRT internal.
        /// </summary>
        /// <param name="subtitleStream">The subtitle stream.</param>
        /// <param name="mediaSource">The input mediaSource.</param>
        /// <param name="outputPath">The output path.</param>
        /// <param name="cancellationToken">The cancellation token.</param>
        /// <returns>Task.</returns>
        /// <exception cref="ArgumentNullException">
        /// The <c>inputPath</c> or <c>outputPath</c> is <c>null</c>.
        /// </exception>
        private async Task ConvertTextSubtitleToSrtInternal(MediaStream subtitleStream, MediaSourceInfo mediaSource, string outputPath, CancellationToken cancellationToken)
        {
            var inputPath = subtitleStream.Path;
            ArgumentException.ThrowIfNullOrEmpty(inputPath);

            ArgumentException.ThrowIfNullOrEmpty(outputPath);

            Directory.CreateDirectory(Path.GetDirectoryName(outputPath) ?? throw new ArgumentException($"Provided path ({outputPath}) is not valid.", nameof(outputPath)));

            var encodingParam = await GetSubtitleFileCharacterSet(subtitleStream, subtitleStream.Language, mediaSource, cancellationToken).ConfigureAwait(false);

            // FFmpeg automatically convert character encoding when it is UTF-16
            // If we specify character encoding, it rejects with "do not specify a character encoding" and "Unable to recode subtitle event"
            if ((inputPath.EndsWith(".smi", StringComparison.Ordinal) || inputPath.EndsWith(".sami", StringComparison.Ordinal)) &&
                (encodingParam.Equals("UTF-16BE", StringComparison.OrdinalIgnoreCase) ||
                 encodingParam.Equals("UTF-16LE", StringComparison.OrdinalIgnoreCase)))
            {
                encodingParam = string.Empty;
            }
            else if (!string.IsNullOrEmpty(encodingParam))
            {
                encodingParam = " -sub_charenc " + encodingParam;
            }

            int exitCode;

            using (var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    FileName = _mediaEncoder.EncoderPath,
                    Arguments = string.Format(CultureInfo.InvariantCulture, "{0} -i \"{1}\" -c:s srt \"{2}\"", encodingParam, inputPath, outputPath),
                    WindowStyle = ProcessWindowStyle.Hidden,
                    ErrorDialog = false
                },
                EnableRaisingEvents = true
            })
            {
                _logger.LogInformation("{0} {1}", process.StartInfo.FileName, process.StartInfo.Arguments);

                try
                {
                    process.Start();
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error starting ffmpeg");

                    throw;
                }

                try
                {
                    var timeoutMinutes = _serverConfigurationManager.GetEncodingOptions().SubtitleExtractionTimeoutMinutes;
                    await process.WaitForExitAsync(TimeSpan.FromMinutes(timeoutMinutes)).ConfigureAwait(false);
                    exitCode = process.ExitCode;
                }
                catch (OperationCanceledException)
                {
                    process.Kill(true);
                    exitCode = -1;
                }
            }

            var failed = false;

            if (exitCode == -1)
            {
                failed = true;

                if (File.Exists(outputPath))
                {
                    try
                    {
                        _logger.LogInformation("Deleting converted subtitle due to failure: {Path}", outputPath);
                        _fileSystem.DeleteFile(outputPath);
                    }
                    catch (IOException ex)
                    {
                        _logger.LogError(ex, "Error deleting converted subtitle {Path}", outputPath);
                    }
                }
            }
            else if (!File.Exists(outputPath))
            {
                failed = true;
            }

            if (failed)
            {
                _logger.LogError("ffmpeg subtitle conversion failed for {Path}", inputPath);

                throw new FfmpegException(
                    string.Format(CultureInfo.InvariantCulture, "ffmpeg subtitle conversion failed for {0}", inputPath));
            }

            await SetAssFont(outputPath, cancellationToken).ConfigureAwait(false);

            _logger.LogInformation("ffmpeg subtitle conversion succeeded for {Path}", inputPath);
        }

        private string GetExtractableSubtitleFormat(MediaStream subtitleStream)
        {
            if (string.Equals(subtitleStream.Codec, "ass", StringComparison.OrdinalIgnoreCase)
                || string.Equals(subtitleStream.Codec, "ssa", StringComparison.OrdinalIgnoreCase)
                || string.Equals(subtitleStream.Codec, "pgssub", StringComparison.OrdinalIgnoreCase))
            {
                return subtitleStream.Codec;
            }
            else
            {
                return "srt";
            }
        }

        private string GetExtractableSubtitleFileExtension(MediaStream subtitleStream)
        {
            // Using .pgssub as file extension is not allowed by ffmpeg. The file extension for pgs subtitles is .sup.
            if (string.Equals(subtitleStream.Codec, "pgssub", StringComparison.OrdinalIgnoreCase))
            {
                return "sup";
            }
            else
            {
                return GetExtractableSubtitleFormat(subtitleStream);
            }
        }

        private bool IsCodecCopyable(string codec)
        {
            return string.Equals(codec, "ass", StringComparison.OrdinalIgnoreCase)
                || string.Equals(codec, "ssa", StringComparison.OrdinalIgnoreCase)
                || string.Equals(codec, "srt", StringComparison.OrdinalIgnoreCase)
                || string.Equals(codec, "subrip", StringComparison.OrdinalIgnoreCase)
                || string.Equals(codec, "pgssub", StringComparison.OrdinalIgnoreCase);
        }

        /// <inheritdoc />
        public async Task ExtractAllExtractableSubtitles(MediaSourceInfo mediaSource, CancellationToken cancellationToken)
        {
            var locks = new List<IDisposable>();
            var extractableStreams = new List<MediaStream>();

            try
            {
                var subtitleStreams = mediaSource.MediaStreams
                    .Where(stream => stream is { IsExtractableSubtitleStream: true, SupportsExternalStream: true });

                foreach (var subtitleStream in subtitleStreams)
                {
                    if (subtitleStream.IsExternal && !subtitleStream.Path.EndsWith(".mks", StringComparison.OrdinalIgnoreCase))
                    {
                        continue;
                    }

                    var outputPath = GetSubtitleCachePath(mediaSource, subtitleStream.Index, "." + GetExtractableSubtitleFileExtension(subtitleStream));

                    var releaser = await _semaphoreLocks.LockAsync(outputPath, cancellationToken).ConfigureAwait(false);

                    if (File.Exists(outputPath))
                    {
                        releaser.Dispose();
                        continue;
                    }

                    locks.Add(releaser);
                    extractableStreams.Add(subtitleStream);
                }

                if (extractableStreams.Count > 0)
                {
                    await ExtractAllExtractableSubtitlesInternal(mediaSource, extractableStreams, cancellationToken).ConfigureAwait(false);
                    await ExtractAllExtractableSubtitlesMKS(mediaSource, extractableStreams, cancellationToken).ConfigureAwait(false);
                }
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Unable to get streams for File:{File}", mediaSource.Path);
            }
            finally
            {
                locks.ForEach(x => x.Dispose());
            }
        }

        private async Task ExtractAllExtractableSubtitlesMKS(
           MediaSourceInfo mediaSource,
           List<MediaStream> subtitleStreams,
           CancellationToken cancellationToken)
        {
            var mksFiles = new List<string>();

            foreach (var subtitleStream in subtitleStreams)
            {
                if (string.IsNullOrEmpty(subtitleStream.Path) || !subtitleStream.Path.EndsWith(".mks", StringComparison.OrdinalIgnoreCase))
                {
                    continue;
                }

                if (!mksFiles.Contains(subtitleStream.Path))
                {
                    mksFiles.Add(subtitleStream.Path);
                }
            }

            if (mksFiles.Count == 0)
            {
                return;
            }

            foreach (string mksFile in mksFiles)
            {
                var inputPath = _mediaEncoder.GetInputArgument(mksFile, mediaSource);
                var outputPaths = new List<string>();
                var args = string.Format(
                    CultureInfo.InvariantCulture,
                    "-i {0} -copyts",
                    inputPath);

                foreach (var subtitleStream in subtitleStreams)
                {
                    if (!subtitleStream.Path.Equals(mksFile, StringComparison.OrdinalIgnoreCase))
                    {
                        continue;
                    }

                    var outputPath = GetSubtitleCachePath(mediaSource, subtitleStream.Index, "." + GetExtractableSubtitleFileExtension(subtitleStream));
                    var outputCodec = IsCodecCopyable(subtitleStream.Codec) ? "copy" : "srt";
                    var streamIndex = EncodingHelper.FindIndex(mediaSource.MediaStreams, subtitleStream);

                    if (streamIndex == -1)
                    {
                        _logger.LogError("Cannot find subtitle stream index for {InputPath} ({Index}), skipping this stream", inputPath, subtitleStream.Index);
                        continue;
                    }

                    Directory.CreateDirectory(Path.GetDirectoryName(outputPath) ?? throw new FileNotFoundException($"Calculated path ({outputPath}) is not valid."));

                    outputPaths.Add(outputPath);
                    args += string.Format(
                        CultureInfo.InvariantCulture,
                        " -map 0:{0} -an -vn -c:s {1} \"{2}\"",
                        streamIndex,
                        outputCodec,
                        outputPath);
                }

                await ExtractSubtitlesForFile(inputPath, args, outputPaths, cancellationToken).ConfigureAwait(false);
            }
        }

        private async Task ExtractAllExtractableSubtitlesInternal(
            MediaSourceInfo mediaSource,
            List<MediaStream> subtitleStreams,
            CancellationToken cancellationToken)
        {
            var inputPath = _mediaEncoder.GetInputArgument(mediaSource.Path, mediaSource);
            var outputPaths = new List<string>();
            var args = string.Format(
                CultureInfo.InvariantCulture,
                "-i {0} -copyts",
                inputPath);

            foreach (var subtitleStream in subtitleStreams)
            {
                if (!string.IsNullOrEmpty(subtitleStream.Path) && subtitleStream.Path.EndsWith(".mks", StringComparison.OrdinalIgnoreCase))
                {
                    _logger.LogDebug("Subtitle {Index} for file {InputPath} is part in an MKS file. Skipping", inputPath, subtitleStream.Index);
                    continue;
                }

                var outputPath = GetSubtitleCachePath(mediaSource, subtitleStream.Index, "." + GetExtractableSubtitleFileExtension(subtitleStream));
                var outputCodec = IsCodecCopyable(subtitleStream.Codec) ? "copy" : "srt";
                var streamIndex = EncodingHelper.FindIndex(mediaSource.MediaStreams, subtitleStream);

                if (streamIndex == -1)
                {
                    _logger.LogError("Cannot find subtitle stream index for {InputPath} ({Index}), skipping this stream", inputPath, subtitleStream.Index);
                    continue;
                }

                Directory.CreateDirectory(Path.GetDirectoryName(outputPath) ?? throw new FileNotFoundException($"Calculated path ({outputPath}) is not valid."));

                outputPaths.Add(outputPath);
                args += string.Format(
                    CultureInfo.InvariantCulture,
                    " -map 0:{0} -an -vn -c:s {1} \"{2}\"",
                    streamIndex,
                    outputCodec,
                    outputPath);
            }

            if (outputPaths.Count == 0)
            {
                return;
            }

            await ExtractSubtitlesForFile(inputPath, args, outputPaths, cancellationToken).ConfigureAwait(false);
        }

        private async Task ExtractSubtitlesForFile(
            string inputPath,
            string args,
            List<string> outputPaths,
            CancellationToken cancellationToken)
        {
            int exitCode;

            using (var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    FileName = _mediaEncoder.EncoderPath,
                    Arguments = args,
                    WindowStyle = ProcessWindowStyle.Hidden,
                    ErrorDialog = false
                },
                EnableRaisingEvents = true
            })
            {
                _logger.LogInformation("{File} {Arguments}", process.StartInfo.FileName, process.StartInfo.Arguments);

                try
                {
                    process.Start();
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error starting ffmpeg");

                    throw;
                }

                try
                {
                    var timeoutMinutes = _serverConfigurationManager.GetEncodingOptions().SubtitleExtractionTimeoutMinutes;
                    await process.WaitForExitAsync(TimeSpan.FromMinutes(timeoutMinutes)).ConfigureAwait(false);
                    exitCode = process.ExitCode;
                }
                catch (OperationCanceledException)
                {
                    process.Kill(true);
                    exitCode = -1;
                }
            }

            var failed = false;

            if (exitCode == -1)
            {
                failed = true;

                foreach (var outputPath in outputPaths)
                {
                    try
                    {
                        _logger.LogWarning("Deleting extracted subtitle due to failure: {Path}", outputPath);
                        _fileSystem.DeleteFile(outputPath);
                    }
                    catch (FileNotFoundException)
                    {
                    }
                    catch (IOException ex)
                    {
                        _logger.LogError(ex, "Error deleting extracted subtitle {Path}", outputPath);
                    }
                }
            }
            else
            {
                foreach (var outputPath in outputPaths)
                {
                    if (!File.Exists(outputPath))
                    {
                        _logger.LogError("ffmpeg subtitle extraction failed for {InputPath} to {OutputPath}", inputPath, outputPath);
                        failed = true;
                        continue;
                    }

                    if (outputPath.EndsWith("ass", StringComparison.OrdinalIgnoreCase))
                    {
                        await SetAssFont(outputPath, cancellationToken).ConfigureAwait(false);
                    }

                    _logger.LogInformation("ffmpeg subtitle extraction completed for {InputPath} to {OutputPath}", inputPath, outputPath);
                }
            }

            if (failed)
            {
                throw new FfmpegException(
                    string.Format(CultureInfo.InvariantCulture, "ffmpeg subtitle extraction failed for {0}", inputPath));
            }
        }

        /// <summary>
        /// Extracts the text subtitle.
        /// </summary>
        /// <param name="mediaSource">The mediaSource.</param>
        /// <param name="subtitleStream">The subtitle stream.</param>
        /// <param name="outputCodec">The output codec.</param>
        /// <param name="outputPath">The output path.</param>
        /// <param name="cancellationToken">The cancellation token.</param>
        /// <returns>Task.</returns>
        /// <exception cref="ArgumentException">Must use inputPath list overload.</exception>
        private async Task ExtractTextSubtitle(
            MediaSourceInfo mediaSource,
            MediaStream subtitleStream,
            string outputCodec,
            string outputPath,
            CancellationToken cancellationToken)
        {
            using (await _semaphoreLocks.LockAsync(outputPath, cancellationToken).ConfigureAwait(false))
            {
                if (!File.Exists(outputPath))
                {
                    var subtitleStreamIndex = EncodingHelper.FindIndex(mediaSource.MediaStreams, subtitleStream);

                    var args = _mediaEncoder.GetInputArgument(mediaSource.Path, mediaSource);

                    if (subtitleStream.IsExternal)
                    {
                        args = _mediaEncoder.GetExternalSubtitleInputArgument(subtitleStream.Path);
                    }

                    await ExtractTextSubtitleInternal(
                        args,
                        subtitleStreamIndex,
                        outputCodec,
                        outputPath,
                        cancellationToken).ConfigureAwait(false);
                }
            }
        }

        private async Task ExtractTextSubtitleInternal(
            string inputPath,
            int subtitleStreamIndex,
            string outputCodec,
            string outputPath,
            CancellationToken cancellationToken)
        {
            ArgumentException.ThrowIfNullOrEmpty(inputPath);

            ArgumentException.ThrowIfNullOrEmpty(outputPath);

            Directory.CreateDirectory(Path.GetDirectoryName(outputPath) ?? throw new ArgumentException($"Provided path ({outputPath}) is not valid.", nameof(outputPath)));

            var processArgs = string.Format(
                CultureInfo.InvariantCulture,
                "-i {0} -copyts -map 0:{1} -an -vn -c:s {2} \"{3}\"",
                inputPath,
                subtitleStreamIndex,
                outputCodec,
                outputPath);

            int exitCode;

            using (var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    FileName = _mediaEncoder.EncoderPath,
                    Arguments = processArgs,
                    WindowStyle = ProcessWindowStyle.Hidden,
                    ErrorDialog = false
                },
                EnableRaisingEvents = true
            })
            {
                _logger.LogInformation("{File} {Arguments}", process.StartInfo.FileName, process.StartInfo.Arguments);

                try
                {
                    process.Start();
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error starting ffmpeg");

                    throw;
                }

                try
                {
                    var timeoutMinutes = _serverConfigurationManager.GetEncodingOptions().SubtitleExtractionTimeoutMinutes;
                    await process.WaitForExitAsync(TimeSpan.FromMinutes(timeoutMinutes)).ConfigureAwait(false);
                    exitCode = process.ExitCode;
                }
                catch (OperationCanceledException)
                {
                    process.Kill(true);
                    exitCode = -1;
                }
            }

            var failed = false;

            if (exitCode == -1)
            {
                failed = true;

                try
                {
                    _logger.LogWarning("Deleting extracted subtitle due to failure: {Path}", outputPath);
                    _fileSystem.DeleteFile(outputPath);
                }
                catch (FileNotFoundException)
                {
                }
                catch (IOException ex)
                {
                    _logger.LogError(ex, "Error deleting extracted subtitle {Path}", outputPath);
                }
            }
            else if (!File.Exists(outputPath))
            {
                failed = true;
            }

            if (failed)
            {
                _logger.LogError("ffmpeg subtitle extraction failed for {InputPath} to {OutputPath}", inputPath, outputPath);

                throw new FfmpegException(
                    string.Format(CultureInfo.InvariantCulture, "ffmpeg subtitle extraction failed for {0} to {1}", inputPath, outputPath));
            }

            _logger.LogInformation("ffmpeg subtitle extraction completed for {InputPath} to {OutputPath}", inputPath, outputPath);

            if (string.Equals(outputCodec, "ass", StringComparison.OrdinalIgnoreCase))
            {
                await SetAssFont(outputPath, cancellationToken).ConfigureAwait(false);
            }
        }

        /// <summary>
        /// Sets the ass font.
        /// </summary>
        /// <param name="file">The file.</param>
        /// <param name="cancellationToken">The token to monitor for cancellation requests. The default value is <c>System.Threading.CancellationToken.None</c>.</param>
        /// <returns>Task.</returns>
        private async Task SetAssFont(string file, CancellationToken cancellationToken = default)
        {
            _logger.LogInformation("Setting ass font within {File}", file);

            string text;
            Encoding encoding;

            using (var fileStream = AsyncFile.OpenRead(file))
            using (var reader = new StreamReader(fileStream, true))
            {
                encoding = reader.CurrentEncoding;

                text = await reader.ReadToEndAsync(cancellationToken).ConfigureAwait(false);
            }

            var newText = text.Replace(",Arial,", ",Arial Unicode MS,", StringComparison.Ordinal);

            if (!string.Equals(text, newText, StringComparison.Ordinal))
            {
                var fileStream = new FileStream(file, FileMode.Create, FileAccess.Write, FileShare.None, IODefaults.FileStreamBufferSize, FileOptions.Asynchronous);
                await using (fileStream.ConfigureAwait(false))
                {
                    var writer = new StreamWriter(fileStream, encoding);
                    await using (writer.ConfigureAwait(false))
                    {
                        await writer.WriteAsync(newText.AsMemory(), cancellationToken).ConfigureAwait(false);
                    }
                }
            }
        }

        private string GetSubtitleCachePath(MediaSourceInfo mediaSource, int subtitleStreamIndex, string outputSubtitleExtension)
        {
            return _pathManager.GetSubtitlePath(mediaSource.Id, subtitleStreamIndex, outputSubtitleExtension);
        }

        /// <inheritdoc />
        public async Task<string> GetSubtitleFileCharacterSet(MediaStream subtitleStream, string language, MediaSourceInfo mediaSource, CancellationToken cancellationToken)
        {
            var subtitleCodec = subtitleStream.Codec;
            var path = subtitleStream.Path;

            if (path.EndsWith(".mks", StringComparison.OrdinalIgnoreCase))
            {
                path = GetSubtitleCachePath(mediaSource, subtitleStream.Index, "." + subtitleCodec);
                await ExtractTextSubtitle(mediaSource, subtitleStream, subtitleCodec, path, cancellationToken)
                    .ConfigureAwait(false);
            }

            var stream = await GetStream(path, mediaSource.Protocol, cancellationToken).ConfigureAwait(false);
            await using (stream.ConfigureAwait(false))
            {
                var result = await CharsetDetector.DetectFromStreamAsync(stream, cancellationToken).ConfigureAwait(false);
                var charset = result.Detected?.EncodingName ?? string.Empty;

                // UTF16 is automatically converted to UTF8 by FFmpeg, do not specify a character encoding
                if ((path.EndsWith(".ass", StringComparison.Ordinal) || path.EndsWith(".ssa", StringComparison.Ordinal) || path.EndsWith(".srt", StringComparison.Ordinal))
                    && (string.Equals(charset, "utf-16le", StringComparison.OrdinalIgnoreCase)
                        || string.Equals(charset, "utf-16be", StringComparison.OrdinalIgnoreCase)))
                {
                    charset = string.Empty;
                }

                _logger.LogDebug("charset {0} detected for {Path}", charset, path);

                return charset;
            }
        }

        private async Task<Stream> GetStream(string path, MediaProtocol protocol, CancellationToken cancellationToken)
        {
            switch (protocol)
            {
                case MediaProtocol.Http:
                    {
                        using var response = await _httpClientFactory.CreateClient(NamedClient.Default)
                            .GetAsync(new Uri(path), cancellationToken)
                            .ConfigureAwait(false);
                        return await response.Content.ReadAsStreamAsync(cancellationToken).ConfigureAwait(false);
                    }

                case MediaProtocol.File:
                    return AsyncFile.OpenRead(path);
                default:
                    throw new ArgumentOutOfRangeException(nameof(protocol));
            }
        }

        public async Task<string> GetSubtitleFilePath(MediaStream subtitleStream, MediaSourceInfo mediaSource, CancellationToken cancellationToken)
        {
            var info = await GetReadableFile(mediaSource, subtitleStream, cancellationToken)
                .ConfigureAwait(false);
            return info.Path;
        }

        /// <inheritdoc />
        public void Dispose()
        {
            _semaphoreLocks.Dispose();
        }

#pragma warning disable CA1034 // Nested types should not be visible
        // Only public for the unit tests
        public readonly record struct SubtitleInfo
        {
            public string Path { get; init; }

            public MediaProtocol Protocol { get; init; }

            public string Format { get; init; }

            public bool IsExternal { get; init; }
        }
    }
}


# Subtitles/ISubtitleWriter.cs
using System.IO;
using System.Threading;
using MediaBrowser.Model.MediaInfo;

namespace MediaBrowser.MediaEncoding.Subtitles
{
    /// <summary>
    /// Interface ISubtitleWriter.
    /// </summary>
    public interface ISubtitleWriter
    {
        /// <summary>
        /// Writes the specified information.
        /// </summary>
        /// <param name="info">The information.</param>
        /// <param name="stream">The stream.</param>
        /// <param name="cancellationToken">The cancellation token.</param>
        void Write(SubtitleTrackInfo info, Stream stream, CancellationToken cancellationToken);
    }
}


# Subtitles/SrtWriter.cs
using System;
using System.Globalization;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using MediaBrowser.Model.MediaInfo;

namespace MediaBrowser.MediaEncoding.Subtitles
{
    /// <summary>
    /// SRT subtitle writer.
    /// </summary>
    public partial class SrtWriter : ISubtitleWriter
    {
        [GeneratedRegex(@"\\n", RegexOptions.IgnoreCase)]
        private static partial Regex NewLineEscapedRegex();

        /// <inheritdoc />
        public void Write(SubtitleTrackInfo info, Stream stream, CancellationToken cancellationToken)
        {
            using (var writer = new StreamWriter(stream, Encoding.UTF8, 1024, true))
            {
                var trackEvents = info.TrackEvents;

                for (int i = 0; i < trackEvents.Count; i++)
                {
                    cancellationToken.ThrowIfCancellationRequested();

                    var trackEvent = trackEvents[i];

                    writer.WriteLine((i + 1).ToString(CultureInfo.InvariantCulture));
                    writer.WriteLine(
                        @"{0:hh\:mm\:ss\,fff} --> {1:hh\:mm\:ss\,fff}",
                        TimeSpan.FromTicks(trackEvent.StartPositionTicks),
                        TimeSpan.FromTicks(trackEvent.EndPositionTicks));

                    var text = trackEvent.Text;

                    // TODO: Not sure how to handle these
                    text = NewLineEscapedRegex().Replace(text, " ");

                    writer.WriteLine(text);
                    writer.WriteLine();
                }
            }
        }
    }
}


# Subtitles/AssWriter.cs
using System;
using System.Globalization;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using MediaBrowser.Model.MediaInfo;

namespace MediaBrowser.MediaEncoding.Subtitles
{
    /// <summary>
    /// ASS subtitle writer.
    /// </summary>
    public partial class AssWriter : ISubtitleWriter
    {
        [GeneratedRegex(@"\n", RegexOptions.IgnoreCase)]
        private static partial Regex NewLineRegex();

        /// <inheritdoc />
        public void Write(SubtitleTrackInfo info, Stream stream, CancellationToken cancellationToken)
        {
            using (var writer = new StreamWriter(stream, Encoding.UTF8, 1024, true))
            {
                var trackEvents = info.TrackEvents;
                var timeFormat = @"hh\:mm\:ss\.ff";

                // Write ASS header
                writer.WriteLine("[Script Info]");
                writer.WriteLine("Title: Jellyfin transcoded ASS subtitle");
                writer.WriteLine("ScriptType: v4.00+");
                writer.WriteLine();
                writer.WriteLine("[V4+ Styles]");
                writer.WriteLine("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding");
                writer.WriteLine("Style: Default,Arial,20,&H00FFFFFF,&H00FFFFFF,&H19333333,&H910E0807,0,0,0,0,100,100,0,0,0,1,0,2,10,10,10,1");
                writer.WriteLine();
                writer.WriteLine("[Events]");
                writer.WriteLine("Format: Layer, Start, End, Style, Text");

                for (int i = 0; i < trackEvents.Count; i++)
                {
                    cancellationToken.ThrowIfCancellationRequested();

                    var trackEvent = trackEvents[i];
                    var startTime = TimeSpan.FromTicks(trackEvent.StartPositionTicks).ToString(timeFormat, CultureInfo.InvariantCulture);
                    var endTime = TimeSpan.FromTicks(trackEvent.EndPositionTicks).ToString(timeFormat, CultureInfo.InvariantCulture);
                    var text = NewLineRegex().Replace(trackEvent.Text, "\\n");

                    writer.WriteLine(
                        "Dialogue: 0,{0},{1},Default,{2}",
                        startTime,
                        endTime,
                        text);
                }
            }
        }
    }
}


# Subtitles/SubtitleEditParser.cs
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using Jellyfin.Extensions;
using MediaBrowser.Model.MediaInfo;
using Microsoft.Extensions.Logging;
using Nikse.SubtitleEdit.Core.Common;
using SubtitleFormat = Nikse.SubtitleEdit.Core.SubtitleFormats.SubtitleFormat;

namespace MediaBrowser.MediaEncoding.Subtitles
{
    /// <summary>
    /// SubStation Alpha subtitle parser.
    /// </summary>
    public class SubtitleEditParser : ISubtitleParser
    {
        private readonly ILogger<SubtitleEditParser> _logger;
        private readonly Dictionary<string, List<Type>> _subtitleFormatTypes;

        /// <summary>
        /// Initializes a new instance of the <see cref="SubtitleEditParser"/> class.
        /// </summary>
        /// <param name="logger">The logger.</param>
        public SubtitleEditParser(ILogger<SubtitleEditParser> logger)
        {
            _logger = logger;
            _subtitleFormatTypes = GetSubtitleFormatTypes();
        }

        /// <inheritdoc />
        public SubtitleTrackInfo Parse(Stream stream, string fileExtension)
        {
            var subtitle = new Subtitle();
            var lines = stream.ReadAllLines().ToList();

            if (!_subtitleFormatTypes.TryGetValue(fileExtension, out var subtitleFormatTypesForExtension))
            {
                throw new ArgumentException($"Unsupported file extension: {fileExtension}", nameof(fileExtension));
            }

            foreach (var subtitleFormatType in subtitleFormatTypesForExtension)
            {
                var subtitleFormat = (SubtitleFormat)Activator.CreateInstance(subtitleFormatType, true)!;
                _logger.LogDebug(
                    "Trying to parse '{FileExtension}' subtitle using the {SubtitleFormatParser} format parser",
                    fileExtension,
                    subtitleFormat.Name);
                subtitleFormat.LoadSubtitle(subtitle, lines, fileExtension);
                if (subtitleFormat.ErrorCount == 0)
                {
                    break;
                }
                else if (subtitleFormat.TryGetErrors(out var errors))
                {
                    _logger.LogError(
                        "{ErrorCount} errors encountered while parsing '{FileExtension}' subtitle using the {SubtitleFormatParser} format parser, errors: {Errors}",
                        subtitleFormat.ErrorCount,
                        fileExtension,
                        subtitleFormat.Name,
                        errors);
                }
                else
                {
                    _logger.LogError(
                        "{ErrorCount} errors encountered while parsing '{FileExtension}' subtitle using the {SubtitleFormatParser} format parser",
                        subtitleFormat.ErrorCount,
                        fileExtension,
                        subtitleFormat.Name);
                }
            }

            if (subtitle.Paragraphs.Count == 0)
            {
                throw new ArgumentException("Unsupported format: " + fileExtension);
            }

            var trackInfo = new SubtitleTrackInfo();
            int len = subtitle.Paragraphs.Count;
            var trackEvents = new SubtitleTrackEvent[len];
            for (int i = 0; i < len; i++)
            {
                var p = subtitle.Paragraphs[i];
                trackEvents[i] = new SubtitleTrackEvent(p.Number.ToString(CultureInfo.InvariantCulture), p.Text)
                {
                    StartPositionTicks = p.StartTime.TimeSpan.Ticks,
                    EndPositionTicks = p.EndTime.TimeSpan.Ticks
                };
            }

            trackInfo.TrackEvents = trackEvents;
            return trackInfo;
        }

        /// <inheritdoc />
        public bool SupportsFileExtension(string fileExtension)
            => _subtitleFormatTypes.ContainsKey(fileExtension);

        private Dictionary<string, List<Type>> GetSubtitleFormatTypes()
        {
            var subtitleFormatTypes = new Dictionary<string, List<Type>>(StringComparer.OrdinalIgnoreCase);
            var assembly = typeof(SubtitleFormat).Assembly;

            foreach (var type in assembly.GetTypes())
            {
                if (!type.IsSubclassOf(typeof(SubtitleFormat)) || type.IsAbstract)
                {
                    continue;
                }

                try
                {
                    var tempInstance = (SubtitleFormat)Activator.CreateInstance(type, true)!;
                    var extension = tempInstance.Extension.TrimStart('.');
                    if (!string.IsNullOrEmpty(extension))
                    {
                        // Store only the type, we will instantiate from it later
                        if (!subtitleFormatTypes.TryGetValue(extension, out var subtitleFormatTypesForExtension))
                        {
                            subtitleFormatTypes[extension] = [type];
                        }
                        else
                        {
                            subtitleFormatTypesForExtension.Add(type);
                        }
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(ex, "Failed to create instance of the subtitle format {SubtitleFormatType}", type.Name);
                }
            }

            return subtitleFormatTypes;
        }
    }
}


# BdInfo/BdInfoExaminer.cs
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using BDInfo;
using Jellyfin.Extensions;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.MediaInfo;

namespace MediaBrowser.MediaEncoding.BdInfo;

/// <summary>
/// Class BdInfoExaminer.
/// </summary>
public class BdInfoExaminer : IBlurayExaminer
{
    private readonly IFileSystem _fileSystem;

    /// <summary>
    /// Initializes a new instance of the <see cref="BdInfoExaminer" /> class.
    /// </summary>
    /// <param name="fileSystem">The filesystem.</param>
    public BdInfoExaminer(IFileSystem fileSystem)
    {
        _fileSystem = fileSystem;
    }

    /// <summary>
    /// Gets the disc info.
    /// </summary>
    /// <param name="path">The path.</param>
    /// <returns>BlurayDiscInfo.</returns>
    public BlurayDiscInfo GetDiscInfo(string path)
    {
        if (string.IsNullOrWhiteSpace(path))
        {
            throw new ArgumentNullException(nameof(path));
        }

        var bdrom = new BDROM(BdInfoDirectoryInfo.FromFileSystemPath(_fileSystem, path));

        bdrom.Scan();

        // Get the longest playlist
        var playlist = bdrom.PlaylistFiles.Values.OrderByDescending(p => p.TotalLength).FirstOrDefault(p => p.IsValid);

        var outputStream = new BlurayDiscInfo
        {
            MediaStreams = Array.Empty<MediaStream>()
        };

        if (playlist is null)
        {
            return outputStream;
        }

        outputStream.Chapters = playlist.Chapters.ToArray();

        outputStream.RunTimeTicks = TimeSpan.FromSeconds(playlist.TotalLength).Ticks;

        var sortedStreams = playlist.SortedStreams;
        var mediaStreams = new List<MediaStream>(sortedStreams.Count);

        for (int i = 0; i < sortedStreams.Count; i++)
        {
            var stream = sortedStreams[i];
            switch (stream)
            {
                case TSVideoStream videoStream:
                    AddVideoStream(mediaStreams, i, videoStream);
                    break;
                case TSAudioStream audioStream:
                    AddAudioStream(mediaStreams, i, audioStream);
                    break;
                case TSTextStream:
                case TSGraphicsStream:
                    AddSubtitleStream(mediaStreams, i, stream);
                    break;
            }
        }

        outputStream.MediaStreams = mediaStreams.ToArray();

        outputStream.PlaylistName = playlist.Name;

        if (playlist.StreamClips is not null && playlist.StreamClips.Count > 0)
        {
            // Get the files in the playlist
            outputStream.Files = playlist.StreamClips.Select(i => i.StreamFile.FileInfo.FullName).ToArray();
        }

        return outputStream;
    }

    /// <summary>
    /// Adds the video stream.
    /// </summary>
    /// <param name="streams">The streams.</param>
    /// <param name="index">The stream index.</param>
    /// <param name="videoStream">The video stream.</param>
    private void AddVideoStream(List<MediaStream> streams, int index, TSVideoStream videoStream)
    {
        var mediaStream = new MediaStream
        {
            BitRate = Convert.ToInt32(videoStream.BitRate),
            Width = videoStream.Width,
            Height = videoStream.Height,
            Codec = GetNormalizedCodec(videoStream),
            IsInterlaced = videoStream.IsInterlaced,
            Type = MediaStreamType.Video,
            Index = index
        };

        if (videoStream.FrameRateDenominator > 0)
        {
            float frameRateEnumerator = videoStream.FrameRateEnumerator;
            float frameRateDenominator = videoStream.FrameRateDenominator;

            mediaStream.AverageFrameRate = mediaStream.RealFrameRate = frameRateEnumerator / frameRateDenominator;
        }

        streams.Add(mediaStream);
    }

    /// <summary>
    /// Adds the audio stream.
    /// </summary>
    /// <param name="streams">The streams.</param>
    /// <param name="index">The stream index.</param>
    /// <param name="audioStream">The audio stream.</param>
    private void AddAudioStream(List<MediaStream> streams, int index, TSAudioStream audioStream)
    {
        var stream = new MediaStream
        {
            Codec = GetNormalizedCodec(audioStream),
            Language = audioStream.LanguageCode,
            ChannelLayout = string.Format(CultureInfo.InvariantCulture, "{0:D}.{1:D}", audioStream.ChannelCount, audioStream.LFE),
            Channels = audioStream.ChannelCount + audioStream.LFE,
            SampleRate = audioStream.SampleRate,
            Type = MediaStreamType.Audio,
            Index = index
        };

        var bitrate = Convert.ToInt32(audioStream.BitRate);

        if (bitrate > 0)
        {
            stream.BitRate = bitrate;
        }

        streams.Add(stream);
    }

    /// <summary>
    /// Adds the subtitle stream.
    /// </summary>
    /// <param name="streams">The streams.</param>
    /// <param name="index">The stream index.</param>
    /// <param name="stream">The stream.</param>
    private void AddSubtitleStream(List<MediaStream> streams, int index, TSStream stream)
    {
        streams.Add(new MediaStream
        {
            Language = stream.LanguageCode,
            Codec = GetNormalizedCodec(stream),
            Type = MediaStreamType.Subtitle,
            Index = index
        });
    }

    private string GetNormalizedCodec(TSStream stream)
        => stream.StreamType switch
        {
            TSStreamType.MPEG1_VIDEO => "mpeg1video",
            TSStreamType.MPEG2_VIDEO => "mpeg2video",
            TSStreamType.VC1_VIDEO => "vc1",
            TSStreamType.AC3_PLUS_AUDIO or TSStreamType.AC3_PLUS_SECONDARY_AUDIO => "eac3",
            TSStreamType.DTS_AUDIO or TSStreamType.DTS_HD_AUDIO or TSStreamType.DTS_HD_MASTER_AUDIO or TSStreamType.DTS_HD_SECONDARY_AUDIO => "dts",
            TSStreamType.PRESENTATION_GRAPHICS => "pgssub",
            _ => stream.CodecShortName
        };
}


# BdInfo/BdInfoFileInfo.cs
using System.IO;
using MediaBrowser.Model.IO;

namespace MediaBrowser.MediaEncoding.BdInfo;

/// <summary>
/// Class BdInfoFileInfo.
/// </summary>
public class BdInfoFileInfo : BDInfo.IO.IFileInfo
{
    private readonly FileSystemMetadata _impl;

    /// <summary>
    /// Initializes a new instance of the <see cref="BdInfoFileInfo" /> class.
    /// </summary>
    /// <param name="impl">The <see cref="FileSystemMetadata" />.</param>
    public BdInfoFileInfo(FileSystemMetadata impl)
    {
        _impl = impl;
    }

    /// <summary>
    /// Gets the name.
    /// </summary>
    public string Name => _impl.Name;

    /// <summary>
    /// Gets the full name.
    /// </summary>
    public string FullName => _impl.FullName;

    /// <summary>
    /// Gets the extension.
    /// </summary>
    public string Extension => _impl.Extension;

    /// <summary>
    /// Gets the length.
    /// </summary>
    public long Length => _impl.Length;

    /// <summary>
    /// Gets a value indicating whether this is a directory.
    /// </summary>
    public bool IsDir => _impl.IsDirectory;

    /// <summary>
    /// Gets a file as file stream.
    /// </summary>
    /// <returns>A <see cref="FileStream" /> for the file.</returns>
    public Stream OpenRead()
    {
        return new FileStream(
            FullName,
            FileMode.Open,
            FileAccess.Read,
            FileShare.Read);
    }

    /// <summary>
    /// Gets a files's content with a stream reader.
    /// </summary>
    /// <returns>A <see cref="StreamReader" /> for the file's content.</returns>
    public StreamReader OpenText()
    {
        return new StreamReader(OpenRead());
    }
}


# BdInfo/BdInfoDirectoryInfo.cs
using System;
using System.IO;
using System.Linq;
using BDInfo.IO;
using MediaBrowser.Model.IO;

namespace MediaBrowser.MediaEncoding.BdInfo;

/// <summary>
/// Class BdInfoDirectoryInfo.
/// </summary>
public class BdInfoDirectoryInfo : IDirectoryInfo
{
    private readonly IFileSystem _fileSystem;

    private readonly FileSystemMetadata _impl;

    /// <summary>
    /// Initializes a new instance of the <see cref="BdInfoDirectoryInfo" /> class.
    /// </summary>
    /// <param name="fileSystem">The filesystem.</param>
    /// <param name="path">The path.</param>
    public BdInfoDirectoryInfo(IFileSystem fileSystem, string path)
    {
        _fileSystem = fileSystem;
        _impl = _fileSystem.GetDirectoryInfo(path);
    }

    private BdInfoDirectoryInfo(IFileSystem fileSystem, FileSystemMetadata impl)
    {
        _fileSystem = fileSystem;
        _impl = impl;
    }

    /// <summary>
    /// Gets the name.
    /// </summary>
    public string Name => _impl.Name;

    /// <summary>
    /// Gets the full name.
    /// </summary>
    public string FullName => _impl.FullName;

    /// <summary>
    /// Gets the parent directory information.
    /// </summary>
    public IDirectoryInfo? Parent
    {
        get
        {
            var parentFolder = Path.GetDirectoryName(_impl.FullName);
            if (parentFolder is not null)
            {
                return new BdInfoDirectoryInfo(_fileSystem, parentFolder);
            }

            return null;
        }
    }

    private static bool IsHidden(ReadOnlySpan<char> name) => name.StartsWith('.');

    /// <summary>
    /// Gets the directories.
    /// </summary>
    /// <returns>An array with all directories.</returns>
    public IDirectoryInfo[] GetDirectories()
    {
        return _fileSystem.GetDirectories(_impl.FullName)
            .Where(d => !IsHidden(d.Name))
            .Select(x => new BdInfoDirectoryInfo(_fileSystem, x))
            .ToArray();
    }

    /// <summary>
    /// Gets the files.
    /// </summary>
    /// <returns>All files of the directory.</returns>
    public IFileInfo[] GetFiles()
    {
        return _fileSystem.GetFiles(_impl.FullName)
            .Where(d => !IsHidden(d.Name))
            .Select(x => new BdInfoFileInfo(x))
            .ToArray();
    }

    /// <summary>
    /// Gets the files matching a pattern.
    /// </summary>
    /// <param name="searchPattern">The search pattern.</param>
    /// <returns>All files of the directory matching the search pattern.</returns>
    public IFileInfo[] GetFiles(string searchPattern)
    {
        return _fileSystem.GetFiles(_impl.FullName, new[] { searchPattern }, false, false)
            .Where(d => !IsHidden(d.Name))
            .Select(x => new BdInfoFileInfo(x))
            .ToArray();
    }

    /// <summary>
    /// Gets the files matching a pattern and search options.
    /// </summary>
    /// <param name="searchPattern">The search pattern.</param>
    /// <param name="searchOption">The search option.</param>
    /// <returns>All files of the directory matching the search pattern and options.</returns>
    public IFileInfo[] GetFiles(string searchPattern, SearchOption searchOption)
    {
        return _fileSystem.GetFiles(
                _impl.FullName,
                new[] { searchPattern },
                false,
                searchOption == SearchOption.AllDirectories)
            .Where(d => !IsHidden(d.Name))
            .Select(x => new BdInfoFileInfo(x))
            .ToArray();
    }

    /// <summary>
    /// Gets the bdinfo of a file system path.
    /// </summary>
    /// <param name="fs">The file system.</param>
    /// <param name="path">The path.</param>
    /// <returns>The BD directory information of the path on the file system.</returns>
    public static IDirectoryInfo FromFileSystemPath(IFileSystem fs, string path)
    {
        return new BdInfoDirectoryInfo(fs, path);
    }
}


# Transcoding/TranscodeManager.cs
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using AsyncKeyedLock;
using Jellyfin.Data;
using Jellyfin.Database.Implementations.Enums;
using Jellyfin.Extensions;
using MediaBrowser.Common;
using MediaBrowser.Common.Configuration;
using MediaBrowser.Common.Extensions;
using MediaBrowser.Controller.Configuration;
using MediaBrowser.Controller.Library;
using MediaBrowser.Controller.MediaEncoding;
using MediaBrowser.Controller.Session;
using MediaBrowser.Controller.Streaming;
using MediaBrowser.Model.Dlna;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.MediaInfo;
using MediaBrowser.Model.Session;
using Microsoft.Extensions.Logging;

namespace MediaBrowser.MediaEncoding.Transcoding;

/// <inheritdoc cref="ITranscodeManager"/>
public sealed class TranscodeManager : ITranscodeManager, IDisposable
{
    private readonly ILoggerFactory _loggerFactory;
    private readonly ILogger<TranscodeManager> _logger;
    private readonly IFileSystem _fileSystem;
    private readonly IApplicationPaths _appPaths;
    private readonly IServerConfigurationManager _serverConfigurationManager;
    private readonly IUserManager _userManager;
    private readonly ISessionManager _sessionManager;
    private readonly EncodingHelper _encodingHelper;
    private readonly IMediaEncoder _mediaEncoder;
    private readonly IMediaSourceManager _mediaSourceManager;
    private readonly IAttachmentExtractor _attachmentExtractor;

    private readonly List<TranscodingJob> _activeTranscodingJobs = new();
    private readonly AsyncKeyedLocker<string> _transcodingLocks = new(o =>
    {
        o.PoolSize = 20;
        o.PoolInitialFill = 1;
    });

    private readonly Version _maxFFmpegCkeyPauseSupported = new Version(6, 1);

    /// <summary>
    /// Initializes a new instance of the <see cref="TranscodeManager"/> class.
    /// </summary>
    /// <param name="loggerFactory">The <see cref="ILoggerFactory"/>.</param>
    /// <param name="fileSystem">The <see cref="IFileSystem"/>.</param>
    /// <param name="appPaths">The <see cref="IApplicationPaths"/>.</param>
    /// <param name="serverConfigurationManager">The <see cref="IServerConfigurationManager"/>.</param>
    /// <param name="userManager">The <see cref="IUserManager"/>.</param>
    /// <param name="sessionManager">The <see cref="ISessionManager"/>.</param>
    /// <param name="encodingHelper">The <see cref="EncodingHelper"/>.</param>
    /// <param name="mediaEncoder">The <see cref="IMediaEncoder"/>.</param>
    /// <param name="mediaSourceManager">The <see cref="IMediaSourceManager"/>.</param>
    /// <param name="attachmentExtractor">The <see cref="IAttachmentExtractor"/>.</param>
    public TranscodeManager(
        ILoggerFactory loggerFactory,
        IFileSystem fileSystem,
        IApplicationPaths appPaths,
        IServerConfigurationManager serverConfigurationManager,
        IUserManager userManager,
        ISessionManager sessionManager,
        EncodingHelper encodingHelper,
        IMediaEncoder mediaEncoder,
        IMediaSourceManager mediaSourceManager,
        IAttachmentExtractor attachmentExtractor)
    {
        _loggerFactory = loggerFactory;
        _fileSystem = fileSystem;
        _appPaths = appPaths;
        _serverConfigurationManager = serverConfigurationManager;
        _userManager = userManager;
        _sessionManager = sessionManager;
        _encodingHelper = encodingHelper;
        _mediaEncoder = mediaEncoder;
        _mediaSourceManager = mediaSourceManager;
        _attachmentExtractor = attachmentExtractor;

        _logger = loggerFactory.CreateLogger<TranscodeManager>();
        DeleteEncodedMediaCache();
        _sessionManager.PlaybackProgress += OnPlaybackProgress;
        _sessionManager.PlaybackStart += OnPlaybackProgress;
    }

    /// <inheritdoc />
    public TranscodingJob? GetTranscodingJob(string playSessionId)
    {
        lock (_activeTranscodingJobs)
        {
            return _activeTranscodingJobs.FirstOrDefault(j => string.Equals(j.PlaySessionId, playSessionId, StringComparison.OrdinalIgnoreCase));
        }
    }

    /// <inheritdoc />
    public TranscodingJob? GetTranscodingJob(string path, TranscodingJobType type)
    {
        lock (_activeTranscodingJobs)
        {
            return _activeTranscodingJobs.FirstOrDefault(j => j.Type == type && string.Equals(j.Path, path, StringComparison.OrdinalIgnoreCase));
        }
    }

    /// <inheritdoc />
    public void PingTranscodingJob(string playSessionId, bool? isUserPaused)
    {
        ArgumentException.ThrowIfNullOrEmpty(playSessionId);

        _logger.LogDebug("PingTranscodingJob PlaySessionId={0} isUsedPaused: {1}", playSessionId, isUserPaused);

        List<TranscodingJob> jobs;

        lock (_activeTranscodingJobs)
        {
            // This is really only needed for HLS.
            // Progressive streams can stop on their own reliably.
            jobs = _activeTranscodingJobs.Where(j => string.Equals(playSessionId, j.PlaySessionId, StringComparison.OrdinalIgnoreCase)).ToList();
        }

        foreach (var job in jobs)
        {
            if (isUserPaused.HasValue)
            {
                _logger.LogDebug("Setting job.IsUserPaused to {0}. jobId: {1}", isUserPaused, job.Id);
                job.IsUserPaused = isUserPaused.Value;
            }

            PingTimer(job, true);
        }
    }

    private void PingTimer(TranscodingJob job, bool isProgressCheckIn)
    {
        if (job.HasExited)
        {
            job.StopKillTimer();
            return;
        }

        var timerDuration = 10000;

        if (job.Type != TranscodingJobType.Progressive)
        {
            timerDuration = 60000;
        }

        job.PingTimeout = timerDuration;
        job.LastPingDate = DateTime.UtcNow;

        // Don't start the timer for playback checkins with progressive streaming
        if (job.Type != TranscodingJobType.Progressive || !isProgressCheckIn)
        {
            job.StartKillTimer(OnTranscodeKillTimerStopped);
        }
        else
        {
            job.ChangeKillTimerIfStarted();
        }
    }

    private async void OnTranscodeKillTimerStopped(object? state)
    {
        var job = state as TranscodingJob ?? throw new ArgumentException($"{nameof(state)} is not of type {nameof(TranscodingJob)}", nameof(state));
        if (!job.HasExited && job.Type != TranscodingJobType.Progressive)
        {
            var timeSinceLastPing = (DateTime.UtcNow - job.LastPingDate).TotalMilliseconds;

            if (timeSinceLastPing < job.PingTimeout)
            {
                job.StartKillTimer(OnTranscodeKillTimerStopped, job.PingTimeout);
                return;
            }
        }

        _logger.LogInformation("Transcoding kill timer stopped for JobId {0} PlaySessionId {1}. Killing transcoding", job.Id, job.PlaySessionId);

        await KillTranscodingJob(job, true, path => true).ConfigureAwait(false);
    }

    /// <inheritdoc />
    public Task KillTranscodingJobs(string deviceId, string? playSessionId, Func<string, bool> deleteFiles)
    {
        var jobs = new List<TranscodingJob>();

        lock (_activeTranscodingJobs)
        {
            // This is really only needed for HLS.
            // Progressive streams can stop on their own reliably.
            jobs.AddRange(_activeTranscodingJobs.Where(j => string.IsNullOrWhiteSpace(playSessionId)
                ? string.Equals(deviceId, j.DeviceId, StringComparison.OrdinalIgnoreCase)
                : string.Equals(playSessionId, j.PlaySessionId, StringComparison.OrdinalIgnoreCase)));
        }

        return Task.WhenAll(GetKillJobs());

        IEnumerable<Task> GetKillJobs()
        {
            foreach (var job in jobs)
            {
                yield return KillTranscodingJob(job, false, deleteFiles);
            }
        }
    }

    private async Task KillTranscodingJob(TranscodingJob job, bool closeLiveStream, Func<string, bool> delete)
    {
        job.DisposeKillTimer();

        _logger.LogDebug("KillTranscodingJob - JobId {0} PlaySessionId {1}. Killing transcoding", job.Id, job.PlaySessionId);

        lock (_activeTranscodingJobs)
        {
            _activeTranscodingJobs.Remove(job);

            if (job.CancellationTokenSource?.IsCancellationRequested == false)
            {
#pragma warning disable CA1849 // Can't await in lock block
                job.CancellationTokenSource.Cancel();
#pragma warning restore CA1849
            }
        }

        job.Stop();

        if (delete(job.Path!))
        {
            await DeletePartialStreamFiles(job.Path!, job.Type, 0, 1500).ConfigureAwait(false);
        }

        if (closeLiveStream && !string.IsNullOrWhiteSpace(job.LiveStreamId))
        {
            await _sessionManager.CloseLiveStreamIfNeededAsync(job.LiveStreamId, job.PlaySessionId).ConfigureAwait(false);
        }
    }

    private async Task DeletePartialStreamFiles(string path, TranscodingJobType jobType, int retryCount, int delayMs)
    {
        if (retryCount >= 10)
        {
            return;
        }

        _logger.LogInformation("Deleting partial stream file(s) {Path}", path);

        await Task.Delay(delayMs).ConfigureAwait(false);

        try
        {
            if (jobType == TranscodingJobType.Progressive)
            {
                DeleteProgressivePartialStreamFiles(path);
            }
            else
            {
                DeleteHlsPartialStreamFiles(path);
            }
        }
        catch (IOException ex)
        {
            _logger.LogError(ex, "Error deleting partial stream file(s) {Path}", path);

            await DeletePartialStreamFiles(path, jobType, retryCount + 1, 500).ConfigureAwait(false);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting partial stream file(s) {Path}", path);
        }
    }

    private void DeleteProgressivePartialStreamFiles(string outputFilePath)
    {
        if (File.Exists(outputFilePath))
        {
            _fileSystem.DeleteFile(outputFilePath);
        }
    }

    private void DeleteHlsPartialStreamFiles(string outputFilePath)
    {
        var directory = Path.GetDirectoryName(outputFilePath)
                        ?? throw new ArgumentException("Path can't be a root directory.", nameof(outputFilePath));

        var name = Path.GetFileNameWithoutExtension(outputFilePath);

        var filesToDelete = _fileSystem.GetFilePaths(directory)
            .Where(f => f.Contains(name, StringComparison.OrdinalIgnoreCase));

        List<Exception>? exs = null;
        foreach (var file in filesToDelete)
        {
            try
            {
                _logger.LogDebug("Deleting HLS file {0}", file);
                _fileSystem.DeleteFile(file);
            }
            catch (IOException ex)
            {
                (exs ??= new List<Exception>()).Add(ex);
                _logger.LogError(ex, "Error deleting HLS file {Path}", file);
            }
        }

        if (exs is not null)
        {
            throw new AggregateException("Error deleting HLS files", exs);
        }
    }

    /// <inheritdoc />
    public void ReportTranscodingProgress(
        TranscodingJob job,
        StreamState state,
        TimeSpan? transcodingPosition,
        float? framerate,
        double? percentComplete,
        long? bytesTranscoded,
        int? bitRate)
    {
        var ticks = transcodingPosition?.Ticks;

        if (job is not null)
        {
            job.Framerate = framerate;
            job.CompletionPercentage = percentComplete;
            job.TranscodingPositionTicks = ticks;
            job.BytesTranscoded = bytesTranscoded;
            job.BitRate = bitRate;
        }

        var deviceId = state.Request.DeviceId;

        if (!string.IsNullOrWhiteSpace(deviceId))
        {
            var audioCodec = state.ActualOutputAudioCodec;
            var videoCodec = state.ActualOutputVideoCodec;
            var hardwareAccelerationType = _serverConfigurationManager.GetEncodingOptions().HardwareAccelerationType;

            _sessionManager.ReportTranscodingInfo(deviceId, new TranscodingInfo
            {
                Bitrate = bitRate ?? state.TotalOutputBitrate,
                AudioCodec = audioCodec,
                VideoCodec = videoCodec,
                Container = state.OutputContainer,
                Framerate = framerate,
                CompletionPercentage = percentComplete,
                Width = state.OutputWidth,
                Height = state.OutputHeight,
                AudioChannels = state.OutputAudioChannels,
                IsAudioDirect = EncodingHelper.IsCopyCodec(state.OutputAudioCodec),
                IsVideoDirect = EncodingHelper.IsCopyCodec(state.OutputVideoCodec),
                HardwareAccelerationType = hardwareAccelerationType,
                TranscodeReasons = state.TranscodeReasons
            });
        }
    }

    /// <inheritdoc />
    public async Task<TranscodingJob> StartFfMpeg(
        StreamState state,
        string outputPath,
        string commandLineArguments,
        Guid userId,
        TranscodingJobType transcodingJobType,
        CancellationTokenSource cancellationTokenSource,
        string? workingDirectory = null)
    {
        var directory = Path.GetDirectoryName(outputPath) ?? throw new ArgumentException($"Provided path ({outputPath}) is not valid.", nameof(outputPath));
        Directory.CreateDirectory(directory);

        await AcquireResources(state, cancellationTokenSource).ConfigureAwait(false);

        if (state.VideoRequest is not null && !EncodingHelper.IsCopyCodec(state.OutputVideoCodec))
        {
            var user = userId.IsEmpty() ? null : _userManager.GetUserById(userId);
            if (user is not null && !user.HasPermission(PermissionKind.EnableVideoPlaybackTranscoding))
            {
                OnTranscodeFailedToStart(outputPath, transcodingJobType, state);

                throw new ArgumentException("User does not have access to video transcoding.");
            }
        }

        ArgumentException.ThrowIfNullOrEmpty(_mediaEncoder.EncoderPath);

        // If subtitles get burned in fonts may need to be extracted from the media file
        if (state.SubtitleStream is not null && (state.SubtitleDeliveryMethod == SubtitleDeliveryMethod.Encode || state.BaseRequest.AlwaysBurnInSubtitleWhenTranscoding))
        {
            if (state.MediaSource.VideoType == VideoType.Dvd || state.MediaSource.VideoType == VideoType.BluRay)
            {
                var concatPath = Path.Join(_appPaths.CachePath, "concat", state.MediaSource.Id + ".concat");
                await _attachmentExtractor.ExtractAllAttachments(concatPath, state.MediaSource, cancellationTokenSource.Token).ConfigureAwait(false);
            }
            else
            {
                await _attachmentExtractor.ExtractAllAttachments(state.MediaPath, state.MediaSource, cancellationTokenSource.Token).ConfigureAwait(false);
            }

            if (state.SubtitleStream.IsExternal && Path.GetExtension(state.SubtitleStream.Path.AsSpan()).Equals(".mks", StringComparison.OrdinalIgnoreCase))
            {
                await _attachmentExtractor.ExtractAllAttachments(state.SubtitleStream.Path, state.MediaSource, cancellationTokenSource.Token).ConfigureAwait(false);
            }
        }

        var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                WindowStyle = ProcessWindowStyle.Hidden,
                CreateNoWindow = true,
                UseShellExecute = false,

                // Must consume both stdout and stderr or deadlocks may occur
                // RedirectStandardOutput = true,
                RedirectStandardError = true,
                RedirectStandardInput = true,
                FileName = _mediaEncoder.EncoderPath,
                Arguments = commandLineArguments,
                WorkingDirectory = string.IsNullOrWhiteSpace(workingDirectory) ? string.Empty : workingDirectory,
                ErrorDialog = false
            },
            EnableRaisingEvents = true
        };

        var transcodingJob = OnTranscodeBeginning(
            outputPath,
            state.Request.PlaySessionId,
            state.MediaSource.LiveStreamId,
            Guid.NewGuid().ToString("N", CultureInfo.InvariantCulture),
            transcodingJobType,
            process,
            state.Request.DeviceId,
            state,
            cancellationTokenSource);

        _logger.LogInformation("{Filename} {Arguments}", process.StartInfo.FileName, process.StartInfo.Arguments);

        var logFilePrefix = "FFmpeg.Transcode-";
        if (state.VideoRequest is not null
            && EncodingHelper.IsCopyCodec(state.OutputVideoCodec))
        {
            logFilePrefix = EncodingHelper.IsCopyCodec(state.OutputAudioCodec)
                ? "FFmpeg.Remux-"
                : "FFmpeg.DirectStream-";
        }

        if (state.VideoRequest is null && EncodingHelper.IsCopyCodec(state.OutputAudioCodec))
        {
            logFilePrefix = "FFmpeg.Remux-";
        }

        var logFilePath = Path.Combine(
            _serverConfigurationManager.ApplicationPaths.LogDirectoryPath,
            $"{logFilePrefix}{DateTime.Now:yyyy-MM-dd_HH-mm-ss}_{state.Request.MediaSourceId}_{Guid.NewGuid().ToString()[..8]}.log");

        // FFmpeg writes debug/error info to stderr. This is useful when debugging so let's put it in the log directory.
        Stream logStream = new FileStream(
            logFilePath,
            FileMode.Create,
            FileAccess.Write,
            FileShare.Read,
            IODefaults.FileStreamBufferSize,
            FileOptions.Asynchronous);

        await JsonSerializer.SerializeAsync(logStream, state.MediaSource, cancellationToken: cancellationTokenSource.Token).ConfigureAwait(false);
        var commandLineLogMessageBytes = Encoding.UTF8.GetBytes(
            Environment.NewLine
            + Environment.NewLine
            + process.StartInfo.FileName + " " + process.StartInfo.Arguments
            + Environment.NewLine
            + Environment.NewLine);

        await logStream.WriteAsync(commandLineLogMessageBytes, cancellationTokenSource.Token).ConfigureAwait(false);

        process.Exited += (_, _) => OnFfMpegProcessExited(process, transcodingJob, state);

        try
        {
            process.Start();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error starting FFmpeg");
            OnTranscodeFailedToStart(outputPath, transcodingJobType, state);

            throw;
        }

        _logger.LogDebug("Launched FFmpeg process");
        state.TranscodingJob = transcodingJob;

        // Important - don't await the log task or we won't be able to kill FFmpeg when the user stops playback
        _ = new JobLogger(_logger).StartStreamingLog(state, process.StandardError, logStream);

        // Wait for the file to exist before proceeding
        var ffmpegTargetFile = state.WaitForPath ?? outputPath;
        _logger.LogDebug("Waiting for the creation of {0}", ffmpegTargetFile);
        while (!File.Exists(ffmpegTargetFile) && !transcodingJob.HasExited)
        {
            await Task.Delay(100, cancellationTokenSource.Token).ConfigureAwait(false);
        }

        _logger.LogDebug("File {0} created or transcoding has finished", ffmpegTargetFile);

        if (state.IsInputVideo && transcodingJob.Type == TranscodingJobType.Progressive && !transcodingJob.HasExited)
        {
            await Task.Delay(1000, cancellationTokenSource.Token).ConfigureAwait(false);

            if (state.ReadInputAtNativeFramerate && !transcodingJob.HasExited)
            {
                await Task.Delay(1500, cancellationTokenSource.Token).ConfigureAwait(false);
            }
        }

        if (!transcodingJob.HasExited)
        {
            StartThrottler(state, transcodingJob);
            StartSegmentCleaner(state, transcodingJob);
        }
        else if (transcodingJob.ExitCode != 0)
        {
            throw new FfmpegException(string.Format(CultureInfo.InvariantCulture, "FFmpeg exited with code {0}", transcodingJob.ExitCode));
        }

        _logger.LogDebug("StartFfMpeg() finished successfully");

        return transcodingJob;
    }

    private void StartThrottler(StreamState state, TranscodingJob transcodingJob)
    {
        if (EnableThrottling(state)
            && (_mediaEncoder.IsPkeyPauseSupported
                || _mediaEncoder.EncoderVersion <= _maxFFmpegCkeyPauseSupported))
        {
            transcodingJob.TranscodingThrottler = new TranscodingThrottler(transcodingJob, _loggerFactory.CreateLogger<TranscodingThrottler>(), _serverConfigurationManager, _fileSystem, _mediaEncoder);
            transcodingJob.TranscodingThrottler.Start();
        }
    }

    private static bool EnableThrottling(StreamState state)
        => state.InputProtocol == MediaProtocol.File
           && state.RunTimeTicks.HasValue
           && state.RunTimeTicks.Value >= TimeSpan.FromMinutes(5).Ticks
           && state.IsInputVideo
           && state.VideoType == VideoType.VideoFile;

    private void StartSegmentCleaner(StreamState state, TranscodingJob transcodingJob)
    {
        if (EnableSegmentCleaning(state))
        {
            transcodingJob.TranscodingSegmentCleaner = new TranscodingSegmentCleaner(transcodingJob, _loggerFactory.CreateLogger<TranscodingSegmentCleaner>(), _serverConfigurationManager, _fileSystem, _mediaEncoder, state.SegmentLength);
            transcodingJob.TranscodingSegmentCleaner.Start();
        }
    }

    private static bool EnableSegmentCleaning(StreamState state)
        => state.InputProtocol is MediaProtocol.File or MediaProtocol.Http
           && state.IsInputVideo
           && state.TranscodingType == TranscodingJobType.Hls
           && state.RunTimeTicks.HasValue
           && state.RunTimeTicks.Value >= TimeSpan.FromMinutes(5).Ticks;

    private TranscodingJob OnTranscodeBeginning(
        string path,
        string? playSessionId,
        string? liveStreamId,
        string transcodingJobId,
        TranscodingJobType type,
        Process process,
        string? deviceId,
        StreamState state,
        CancellationTokenSource cancellationTokenSource)
    {
        lock (_activeTranscodingJobs)
        {
            var job = new TranscodingJob(_loggerFactory.CreateLogger<TranscodingJob>())
            {
                Type = type,
                Path = path,
                Process = process,
                ActiveRequestCount = 1,
                DeviceId = deviceId,
                CancellationTokenSource = cancellationTokenSource,
                Id = transcodingJobId,
                PlaySessionId = playSessionId,
                LiveStreamId = liveStreamId,
                MediaSource = state.MediaSource
            };

            _activeTranscodingJobs.Add(job);

            ReportTranscodingProgress(job, state, null, null, null, null, null);

            return job;
        }
    }

    /// <inheritdoc />
    public void OnTranscodeEndRequest(TranscodingJob job)
    {
        job.ActiveRequestCount--;
        _logger.LogDebug("OnTranscodeEndRequest job.ActiveRequestCount={ActiveRequestCount}", job.ActiveRequestCount);
        if (job.ActiveRequestCount <= 0)
        {
            PingTimer(job, false);
        }
    }

    private void OnTranscodeFailedToStart(string path, TranscodingJobType type, StreamState state)
    {
        lock (_activeTranscodingJobs)
        {
            var job = _activeTranscodingJobs.FirstOrDefault(j => j.Type == type && string.Equals(j.Path, path, StringComparison.OrdinalIgnoreCase));

            if (job is not null)
            {
                _activeTranscodingJobs.Remove(job);
            }
        }

        if (!string.IsNullOrWhiteSpace(state.Request.DeviceId))
        {
            _sessionManager.ClearTranscodingInfo(state.Request.DeviceId);
        }
    }

    private void OnFfMpegProcessExited(Process process, TranscodingJob job, StreamState state)
    {
        job.HasExited = true;
        job.ExitCode = process.ExitCode;

        ReportTranscodingProgress(job, state, null, null, null, null, null);

        _logger.LogDebug("Disposing stream resources");
        state.Dispose();

        if (process.ExitCode == 0)
        {
            _logger.LogInformation("FFmpeg exited with code 0");
        }
        else
        {
            _logger.LogError("FFmpeg exited with code {0}", process.ExitCode);
        }

        job.Dispose();
    }

    private async Task AcquireResources(StreamState state, CancellationTokenSource cancellationTokenSource)
    {
        if (state.MediaSource.RequiresOpening && string.IsNullOrWhiteSpace(state.Request.LiveStreamId))
        {
            var liveStreamResponse = await _mediaSourceManager.OpenLiveStream(
                    new LiveStreamRequest { OpenToken = state.MediaSource.OpenToken },
                    cancellationTokenSource.Token)
                .ConfigureAwait(false);
            var encodingOptions = _serverConfigurationManager.GetEncodingOptions();

            _encodingHelper.AttachMediaSourceInfo(state, encodingOptions, liveStreamResponse.MediaSource, state.RequestedUrl);

            if (state.VideoRequest is not null)
            {
                _encodingHelper.TryStreamCopy(state);
            }
        }

        if (state.MediaSource.BufferMs.HasValue)
        {
            await Task.Delay(state.MediaSource.BufferMs.Value, cancellationTokenSource.Token).ConfigureAwait(false);
        }
    }

    /// <inheritdoc />
    public TranscodingJob? OnTranscodeBeginRequest(string path, TranscodingJobType type)
    {
        lock (_activeTranscodingJobs)
        {
            var job = _activeTranscodingJobs
                .FirstOrDefault(j => j.Type == type && string.Equals(j.Path, path, StringComparison.OrdinalIgnoreCase));

            if (job is null)
            {
                return null;
            }

            job.ActiveRequestCount++;
            if (string.IsNullOrWhiteSpace(job.PlaySessionId) || job.Type == TranscodingJobType.Progressive)
            {
                job.StopKillTimer();
            }

            return job;
        }
    }

    private void OnPlaybackProgress(object? sender, PlaybackProgressEventArgs e)
    {
        if (!string.IsNullOrWhiteSpace(e.PlaySessionId))
        {
            PingTranscodingJob(e.PlaySessionId, e.IsPaused);
        }
    }

    private void DeleteEncodedMediaCache()
    {
        var path = _serverConfigurationManager.GetTranscodePath();
        if (!Directory.Exists(path))
        {
            return;
        }

        foreach (var file in _fileSystem.GetFilePaths(path, true))
        {
            try
            {
                _fileSystem.DeleteFile(file);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting encoded media cache file {Path}", path);
            }
        }
    }

    /// <summary>
    /// Transcoding lock.
    /// </summary>
    /// <param name="outputPath">The output path of the transcoded file.</param>
    /// <param name="cancellationToken">The cancellation token.</param>
    /// <returns>An <see cref="IDisposable"/>.</returns>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public ValueTask<IDisposable> LockAsync(string outputPath, CancellationToken cancellationToken)
    {
        return _transcodingLocks.LockAsync(outputPath, cancellationToken);
    }

    /// <inheritdoc />
    public void Dispose()
    {
        _sessionManager.PlaybackProgress -= OnPlaybackProgress;
        _sessionManager.PlaybackStart -= OnPlaybackProgress;
        _transcodingLocks.Dispose();
    }
}


# Properties/AssemblyInfo.cs
using System.Reflection;
using System.Resources;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;

// General Information about an assembly is controlled through the following
// set of attributes. Change these attribute values to modify the information
// associated with an assembly.
[assembly: AssemblyTitle("MediaBrowser.MediaEncoding")]
[assembly: AssemblyDescription("")]
[assembly: AssemblyConfiguration("")]
[assembly: AssemblyCompany("Jellyfin Project")]
[assembly: AssemblyProduct("Jellyfin Server")]
[assembly: AssemblyCopyright("Copyright ©  2019 Jellyfin Contributors. Code released under the GNU General Public License")]
[assembly: AssemblyTrademark("")]
[assembly: AssemblyCulture("")]
[assembly: NeutralResourcesLanguage("en")]
[assembly: InternalsVisibleTo("Jellyfin.MediaEncoding.Tests")]

// Setting ComVisible to false makes the types in this assembly not visible
// to COM components.  If you need to access a type in this assembly from
// COM, set the ComVisible attribute to true on that type.
[assembly: ComVisible(false)]


